from pathlib import Path

lmentry_random_seed = 1407

ROOT_DIR = Path(__file__).parent.parent

SYSTEM_PROMPT = {
    "en": "You are a helpful assistant. Answer concisely and correctly.",
    "it": "Sei un assistente utile. Rispondi in modo conciso e corretto.",
    "ca": "Ets un assistent útil. Repon de forma concisa i correcta.",
    "es": "Eres un asistente útil. Responde de forma concisa y correcta.",
    "eu": "Laguntzaile erabilgarri bat zara. Erantzun laburki eta zuzen.",
    "gl": "Vostede é un asistente útil. Responde de forma concisa e correcta.",
    "ko": "당신은 유용한 보조 역할을 수행해야합니다. 간결하고 정확하게 답변해 주세요.",
    "de": "Sie sind ein hilfreicher Assistent. Antworten Sie präzise und richtig.",
    "pt_br": "Você é um assistente prestativo. Responda de forma concisa e correta."
}

paper_models = {
    "Llama-3_1-8B-Instruct" : {"short_name": "Llama-3.1-8B-Instruct", "paper_name": "Llama-3.1-8B-Instruct", "predictor_name": "meta-llama/Llama-3.1-8B-Instruct"},
    "Llama-3_2-1B-Instruct" : {"short_name": "Llama-3.2-1B-Instruct", "paper_name": "Llama-3.2-1B-Instruct", "predictor_name": "meta-llama/Llama-3.2-1B-Instruct"},
    "Llama-3_2-3B-Instruct" : {"short_name": "Llama-3.2-3B-Instruct", "paper_name": "Llama-3.2-3B-Instruct", "predictor_name": "meta-llama/Llama-3.2-3B-Instruct"},
    "Qwen2_5-1_5B-Instruct" : {"short_name": "Qwen2.5-1.5B-Instruct", "paper_name": "Qwen2.5-1.5B-Instruct", "predictor_name": "Qwen/Qwen2.5-1.5B-Instruct"},
    "Qwen2_5-3B-Instruct" : {"short_name": "Qwen2.5-3B-Instruct", "paper_name": "Qwen2.5-3B-Instruct", "predictor_name": "Qwen/Qwen2.5-3B-Instruct"},
    "Qwen2_5-7B-Instruct" : {"short_name": "Qwen2.5-7B-Instruct", "paper_name": "Qwen2.5-7B-Instruct", "predictor_name": "Qwen/Qwen2.5-7B-Instruct"},
    "salamandra-2b-instruct" : {"short_name": "salamandra-2b-instruct", "paper_name": "salamandra-2b-instruct", "predictor_name": "BSC-LT/salamandra-2b-instruct"},
    "EuroLLM-1_7B-Instruct" : {"short_name": "EuroLLM-1.7B-Instruct", "paper_name": "EuroLLM-1.7B-Instruct", "predictor_name": "utter-project/EuroLLM-1.7B-Instruct"},
    "EuroLLM-9B-Instruct" : {"short_name": "EuroLLM-9B-Instruct", "paper_name": "EuroLLM-9B-Instruct", "predictor_name": "utter-project/EuroLLM-9B-Instruct"},
    "Teuken-7B-instruct-commercial-v0_4" : {"short_name": "Teuken-7B-instruct-commercial-v0.4", "paper_name": "Teuken-7B-instruct-commercial-v0.4", "predictor_name": "openGPT-X/Teuken-7B-instruct-commercial-v0.4"},
    "occiglot-7b-eu5-instruct" : {"short_name": "occiglot-7b-eu5-instruct", "paper_name": "occiglot-7b-eu5-instruct", "predictor_name": "occiglot/occiglot-7b-eu5-instruct"},
    "LLaMAntino-3-ANITA-8B-Inst-DPO-ITA" : {"short_name": "LLaMAntino-3-ANITA-8B-Inst-DPO-ITA", "paper_name": "LLaMAntino-3-ANITA-8B-Inst-DPO-ITA", "predictor_name": "swap-uniba/LLaMAntino-3-ANITA-8B-Inst-DPO-ITA"},
    "Latxa-Llama-3_1-8B-Instruct" : {"short_name": "Latxa-Llama-3.1-8B-Instruct", "paper_name": "Latxa-Llama-3.1-8B-Instruct", "predictor_name": "HiTZ/Latxa-Llama-3.1-8B-Instruct"},
    "occiglot-7b-es-en-instruct" : {"short_name": "occiglot-7b-es-en-instruct", "paper_name": "occiglot-7b-es-en-instruct", "predictor_name": "occiglot/occiglot-7b-es-en-instruct"},
    "EXAONE-3_5-7_8B-Instruct" : {"short_name": "EXAONE-3.5-7.8B-Instruct", "paper_name": "EXAONE-3.5-7.8B-Instruct", "predictor_name": "LGAI-EXAONE/EXAONE-3.5-7.8B-Instruct"},
    "SmolLM2-360M-Instruct" : {"short_name": "SmolLM2-360M-Instruct", "paper_name": "SmolLM2-360M-Instruct", "predictor_name": "HuggingFaceTB/SmolLM2-360M-Instruct"},
    "SmolLM2-1_7B-Instruct" : {"short_name": "SmolLM2-1.7B-Instruct", "paper_name": "SmolLM2-1.7B-Instruct", "predictor_name": "HuggingFaceTB/SmolLM2-1.7B-Instruct"},
    "minerva-7b-instruct" : {"short_name": "minerva-7b-instruct", "paper_name": "minerva-7b-instruct", "predictor_name": "sapienzanlp/Minerva-7B-instruct-v1.0"},
}

simple_answer_index_task_names = [
    "more_letters", "less_letters", "first_alphabetically",
    "rhyming_word", "homophones", "bigger_number", "smaller_number"
]

eu_abstract_categories = {
    "bizitza",
    "garraio",
    "gizarte",
    "etxe",
    "gizarte",
    "geografia",
    "jende",
    "familia",
    "espazio eta kopuru",
    "ekonomia",
    "giza gorputz"
}

#### GLOBAL VARIABLES

LANG = None # Choose between ca, de, en, es, eu, gl, ko, it OR pt_br.
PROMPT_LANG = None # Choose between ca, de, en, es, eu, gl, ko, it OR pt_br.
TASKS_DATA_DIR = None
PREDICTIONS_ROOT_DIR = None
RESULTS_DIR = None
VISUALIZATIONS_DIR = None
SCORER_EVALUATION_DIR = None
RESOURCES_DIR = None
LMENTRY_WORDS_PATH = None
RHYME_GROUPS_PATH = None
HOMOPHONES_PATH = None
PHONETICALLY_UNAMBIGUOUS_WORDS_PATH = None


def initialize_variables(lang):

    global LANG
    global PROMPT_LANG
    global TASKS_DATA_DIR
    global PREDICTIONS_ROOT_DIR
    global RESULTS_DIR
    global VISUALIZATIONS_DIR
    global SCORER_EVALUATION_DIR
    global RESOURCES_DIR
    global LMENTRY_WORDS_PATH
    global RHYME_GROUPS_PATH
    global HOMOPHONES_PATH
    global PHONETICALLY_UNAMBIGUOUS_WORDS_PATH

    print("LANG:", lang)

    LANG = lang # Choose between ca, de, en, es, eu, gl, ko, it OR pt_br.

    PROMPT_LANG = lang # Choose between ca, de, en, es, eu, gl, ko, it OR pt_br.

    TASKS_DATA_DIR = ROOT_DIR.joinpath(f"data/{LANG}")
    PREDICTIONS_ROOT_DIR = ROOT_DIR.joinpath(f"predictions/{LANG}")
    RESULTS_DIR = ROOT_DIR.joinpath(f"results/{LANG}")
    VISUALIZATIONS_DIR = RESULTS_DIR.joinpath("visualizations")
    SCORER_EVALUATION_DIR = RESULTS_DIR.joinpath("scorer_evaluation")
    RESOURCES_DIR = ROOT_DIR.joinpath(f"resources/{LANG}")
    LMENTRY_WORDS_PATH = RESOURCES_DIR.joinpath("lmentry_words.json")
    RHYME_GROUPS_PATH = RESOURCES_DIR.joinpath("rhyme_groups.json")
    HOMOPHONES_PATH = RESOURCES_DIR.joinpath("homophones.csv")
    PHONETICALLY_UNAMBIGUOUS_WORDS_PATH = RESOURCES_DIR.joinpath("phonetically_unambiguous_words.json")

def get_short_model_name(model_name: str):
    return paper_models[model_name]["short_name"]


def get_predictor_model_name(model_name: str):
    return paper_models[model_name].get("predictor_name", model_name)


def get_paper_model_name(model_name: str):
    return paper_models[model_name]["paper_name"]