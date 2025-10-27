import json
import logging
import os
import time
from itertools import repeat
from multiprocessing import Pool
from pathlib import Path
from typing import List
from tqdm import tqdm

import openai
import torch
from transformers import AutoModelForSeq2SeqLM, PreTrainedModel, AutoTokenizer, AutoModelForCausalLM

from lmentry.constants import get_predictor_model_name, SYSTEM_PROMPT, LANG, PROMPT_LANG
from lmentry.tasks.lmentry_tasks import all_tasks

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%Y/%m/%d %H:%M:%S', level=logging.INFO)


def _batcher(sequence, batch_size):
    # return a list of strings,
    # each element of the batch is an input where the model is asked to continue properly.

    for i in range(0, len(sequence), batch_size):
        yield sequence[i:i + batch_size]


def _chatter(strings, tokenizer):
    strings_chatter = []

    system_prompt = SYSTEM_PROMPT[PROMPT_LANG]

    print(f"Selected system prompt: '{system_prompt}'")

    for text in strings:
        
        # apply messages structure
        messages = [
            {"role": "system", "content": system_prompt}, # Original: 'You are a helpful assistant. Please give a long and detailed answer.'
            {"role": "user", "content": text},
        ]

        chat_text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True, return_dict=False)
        strings_chatter.append(chat_text)

    return strings_chatter


def _ms_since_epoch():
    return time.perf_counter_ns() // 1000000


def generate_task_hf_predictions(task_name, model: PreTrainedModel = None,
                                model_name="", max_new_tokens=128, batch_size=100,
                                data_path=None, output_path=None):
    task = all_tasks[task_name]()

    if not model_name and not model:
        raise ValueError("must provide either `model_name` or `model`")

    hf_model_name = model.name_or_path if model else get_predictor_model_name(model_name)

    logging.info(f"generating predictions for task \"{task_name}\" with model \"{hf_model_name}\"")

    # initialize tokenizer and model
    device = torch.device("cuda") if torch.cuda.is_available() else "cpu"
    print(f"Device: {device}")
    tokenizer = AutoTokenizer.from_pretrained(hf_model_name, padding_side='left')
    tokenizer.add_special_tokens({'pad_token': tokenizer.eos_token}) # added <- DO WE NEED THIS OUTSIDE OF GPT2?

    # load task data
    data_path = data_path or task.default_data_path
    print(f"Data path: {data_path}")
    with open(data_path) as f_examples:
        data = json.load(f_examples)
    # get the inputs from the task data
    examples = data["examples"]
    string_inputs = [example["input"] for example in examples.values()]
    batch_size = min(batch_size, len(string_inputs))
    print(f"Batch size: {batch_size}")
    print(f"String inputs: {len(string_inputs)}")
    stop_strings = [] # for instruction tuned models, we want to generate until stopping condition is raised.

    #  apply chat template.
    if tokenizer.chat_template:
        # for each string in the batch apply chat template, do it sequentially.
        string_inputs = _chatter(string_inputs, tokenizer=tokenizer)

    # generate predictions
    predictions: list[str] = []

    for batch_of_strings in _batcher(string_inputs, batch_size):
        batched_encoding = tokenizer(batch_of_strings, padding="longest", return_tensors="pt", add_special_tokens=False).to(device) # add_special_tokens=False, are already added by the chat template
        # tensor_inputs = batched_encoding["input_ids"] <- THIS IS NOT USED BUT IT IS IN THE ORIGINAL CODE!
        tensor_outputs = model.generate(**batched_encoding, max_new_tokens=max_new_tokens, temperature=0.0, do_sample=False) # to use in a more efficient way the regex to evaluate our models, greedy deconding and tempre
        tensor_outputs_without_inputs = tensor_outputs[:, batched_encoding["input_ids"].shape[1]:] #Added this to remove input from output.
        outputs = tokenizer.batch_decode(tensor_outputs_without_inputs, skip_special_tokens=True) #Modified for the same reason.
        predictions.extend(outputs)
        logging.info(f"generated {len(predictions)} predictions for {task.name}")
        
    # save the predictions
    predictions_data = dict()
    for id_, input_, prediction in zip(examples, string_inputs, predictions):
        predictions_data[id_] = {"input": input_, "prediction": prediction}

    output_path = output_path or task.predictions_dir.joinpath(model_name).with_suffix(".json")
    with open(output_path, "w", encoding="utf-8") as f_predictions:
        json.dump(predictions_data, f_predictions, indent=2, ensure_ascii=False)


def generate_all_hf_predictions(task_names: List[str] = None, model_name: str = "",
                                max_new_tokens=64, batch_size=256): #CHANGED FROM 100.

    task_names = task_names or all_tasks
    hf_model_name = get_predictor_model_name(model_name)
    logging.info(f"loading model {hf_model_name}")
    
    #device = torch.device("cuda") if torch.cuda.is_available() else "cpu"
    model = AutoModelForCausalLM.from_pretrained(hf_model_name, device_map="auto", torch_dtype=torch.bfloat16, attn_implementation="flash_attention_2") # torch_dtype=torch.float16

    logging.info(f"finished loading model {hf_model_name}")
    for task_name in task_names:
        generate_task_hf_predictions(task_name, model, model_name, max_new_tokens, batch_size)