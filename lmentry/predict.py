import json
import logging
import os
import time
from itertools import repeat
from multiprocessing import Pool
from pathlib import Path
from typing import List
from tqdm import tqdm
import argparse

import openai
import torch

from transformers import AutoModelForSeq2SeqLM, PreTrainedModel, AutoTokenizer, AutoModelForCausalLM
from datasets import load_dataset
from vllm import LLM, SamplingParams

from lmentry.system_prompts import SYSTEM_PROMPT
from lmentry.models import get_predictor_model_name
from lmentry.constants import initialize_variables

os.environ["VLLM_WORKER_MULTIPROC_METHOD"] = "spawn" # NEEDED if VLLM raise some fork process errors

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%Y/%m/%d %H:%M:%S', level=logging.INFO)

LANG = None

def _batcher(sequence, batch_size):
    # return a list of strings,
    # each element of the batch is an input where the model is asked to continue properly.

    for i in range(0, len(sequence), batch_size):
        yield sequence[i:i + batch_size]


def _chatter(strings, tokenizer):
    strings_chatter = []

    system_prompt = SYSTEM_PROMPT[LANG]

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
                                model_name="", max_new_tokens=128, batch_size=100, output_path=None, use_vllm=False):
    from lmentry.tasks.lmentry_tasks import all_tasks

    task = all_tasks[task_name]()

    if not model_name and not model:
        raise ValueError("must provide either `model_name` or `model`")

    hf_model_name = get_predictor_model_name(model_name)

    logging.info(f"generating predictions for task \"{task_name}\" with model \"{hf_model_name}\"")

    # initialize tokenizer and model
    device = torch.device("cuda") if torch.cuda.is_available() else "cpu"
    print(f"Device: {device}")
    tokenizer = AutoTokenizer.from_pretrained(hf_model_name, padding_side='left')
    tokenizer.add_special_tokens({'pad_token': tokenizer.eos_token}) # added <- DO WE NEED THIS OUTSIDE OF GPT2?

    # LOAD THE DATASET
    ds = load_dataset(
        "BSC-LT/multi_lmentry",
        LANG,
        data_files=f"{LANG}/{task.name}.jsonl"
    )["train"]

    string_inputs = [example for example in ds["input"]]

    #  apply chat template.
    if tokenizer.chat_template:
        # for each string in the batch apply chat template, do it sequentially.
        string_inputs = _chatter(string_inputs, tokenizer=tokenizer)

    print(f"String inputs: {len(string_inputs)}")

    predictions: list[str] = []

    if use_vllm:
        sampling_params = SamplingParams(temperature=0, max_tokens=max_new_tokens)

        outputs = model.generate(string_inputs, sampling_params)

        for output in outputs:
            prompt = output.prompt
            generated_text = output.outputs[0].text
            predictions.append(generated_text)

    else: # generate predictions with HF, batch wise
        batch_size = min(batch_size, len(string_inputs))
        print(f"Batch size: {batch_size}")
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
    for id_, input_, prediction in zip(ds["id"], string_inputs, predictions):
        predictions_data[id_] = {"input": input_, "prediction": prediction}

    output_path = output_path or task.predictions_dir.joinpath(model_name).with_suffix(".json")
    with open(output_path, "w", encoding="utf-8") as f_predictions:
        json.dump(predictions_data, f_predictions, indent=2, ensure_ascii=False)


def generate_all_hf_predictions(model, task_names: List[str] = None, model_name: str = "",
                                max_new_tokens=64, batch_size=256, use_vllm=False):
    for task_name in task_names:
        generate_task_hf_predictions(task_name, model, model_name, max_new_tokens, batch_size, use_vllm=use_vllm)


def main(args):
    global LANG
    lang = args.language
    models = args.model_list
    use_vllm = args.use_vllm

    ## initialize the global variables
    initialize_variables(lang)
    LANG = lang
    ## ----

    print("#"*30)
    print("Testing the following models:\n", models)
    print("Testing the Language:", lang)
    print("#"*30)

    for model_name in models:
        hf_model_name = get_predictor_model_name(model_name)
        logging.info(f"loading model {hf_model_name}")
        
        if use_vllm:
            model = LLM(model=hf_model_name, dtype=torch.bfloat16)
        else:
            model = AutoModelForCausalLM.from_pretrained(hf_model_name, device_map="auto", torch_dtype=torch.bfloat16, attn_implementation="flash_attention_2")

        logging.info(f"finished loading model {hf_model_name}")

        if lang == "eu":
            #for eu
            generate_all_hf_predictions(model, task_names=["sentence_containing","sentence_not_containing","word_containing","word_not_containing","most_associated_word","least_associated_word","any_words_from_category","all_words_from_category","first_alphabetically","more_letters","less_letters","bigger_number"], model_name=model_name, use_vllm=use_vllm)
            generate_all_hf_predictions(model, task_names=["smaller_number","rhyming_word","word_after","word_before","starts_with_word","ends_with_word","starts_with_letter","ends_with_letter","first_word","last_word","first_letter","last_letter"], model_name=model_name, use_vllm=use_vllm)
            generate_all_hf_predictions(model, task_names=["first_alphabetically_far_first_letter","first_alphabetically_different_first_letter","first_alphabetically_consecutive_first_letter","first_alphabetically_same_first_letter","any_words_from_category_5_distractors","any_words_from_category_4_distractors","any_words_from_category_3_distractors","all_words_from_category_0_distractors"], model_name=model_name, use_vllm=use_vllm)
            generate_all_hf_predictions(model, task_names=["all_words_from_category_1_distractors","all_words_from_category_2_distractors","rhyming_word_orthographically_similar","more_letters_length_diff_3plus","more_letters_length_diff_1","less_letters_length_diff_3plus","less_letters_length_diff_1"], model_name=model_name, use_vllm=use_vllm)
        elif lang == "en":
            # for en
            generate_all_hf_predictions(model, task_names=["sentence_containing","sentence_not_containing","word_containing","word_not_containing","most_associated_word","least_associated_word","any_words_from_category","all_words_from_category","first_alphabetically","more_letters","less_letters","bigger_number"], model_name=model_name, use_vllm=use_vllm)
            generate_all_hf_predictions(model, task_names=["smaller_number","rhyming_word","homophones","word_after","word_before","starts_with_word","ends_with_word","starts_with_letter","ends_with_letter","first_word","last_word","first_letter","last_letter"], model_name=model_name, use_vllm=use_vllm)
            generate_all_hf_predictions(model, task_names=["first_alphabetically_far_first_letter","first_alphabetically_different_first_letter","first_alphabetically_consecutive_first_letter","first_alphabetically_same_first_letter","any_words_from_category_5_distractors","any_words_from_category_4_distractors","any_words_from_category_3_distractors","all_words_from_category_0_distractors"], model_name=model_name, use_vllm=use_vllm)
            generate_all_hf_predictions(model, task_names=["all_words_from_category_1_distractors","all_words_from_category_2_distractors","rhyming_word_orthographically_similar","more_letters_length_diff_3plus","more_letters_length_diff_1","less_letters_length_diff_3plus","less_letters_length_diff_1"], model_name=model_name, use_vllm=use_vllm)
            generate_all_hf_predictions(model, task_names=["rhyming_word_orthographically_different"], model_name=model_name, use_vllm=use_vllm)
            generate_all_hf_predictions(model, task_names=["all_words_from_category_1_distractors","all_words_from_category_2_distractors","rhyming_word_orthographically_similar","more_letters_length_diff_3plus","more_letters_length_diff_1","less_letters_length_diff_3plus","less_letters_length_diff_1"], model_name=model_name, use_vllm=use_vllm)
        else:
            generate_all_hf_predictions(model, task_names=["sentence_containing","sentence_not_containing","word_containing","word_not_containing","most_associated_word","least_associated_word","any_words_from_category","all_words_from_category","first_alphabetically","more_letters","less_letters","bigger_number"], model_name=model_name, use_vllm=use_vllm)
            generate_all_hf_predictions(model, task_names=["smaller_number","rhyming_word","homophones","word_after","word_before","starts_with_word","ends_with_word","starts_with_letter","ends_with_letter","first_word","last_word","first_letter","last_letter"], model_name=model_name, use_vllm=use_vllm)
            generate_all_hf_predictions(model, task_names=["first_alphabetically_far_first_letter","first_alphabetically_different_first_letter","first_alphabetically_consecutive_first_letter","first_alphabetically_same_first_letter","any_words_from_category_5_distractors","any_words_from_category_4_distractors","any_words_from_category_3_distractors","all_words_from_category_0_distractors"], model_name=model_name, use_vllm=use_vllm)
            generate_all_hf_predictions(model, task_names=["all_words_from_category_1_distractors","all_words_from_category_2_distractors","rhyming_word_orthographically_similar","more_letters_length_diff_3plus","more_letters_length_diff_1","less_letters_length_diff_3plus","less_letters_length_diff_1"], model_name=model_name, use_vllm=use_vllm)

        del model

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='Execute Prediction'
                    )
    parser.add_argument('-l', '--language', type=str, required=True)
    parser.add_argument('-m', '--model_list', nargs='+', required=True)
    parser.add_argument('-v', '--use_vllm', action="store_true")
    args = parser.parse_args()
    main(args)