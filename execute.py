from lmentry.constants import initialize_variables
import argparse

#######################--MODELS--#######################

#multi
#model='BLOOM-1B7'
#model='BLOOM-7B1'
#model='BLOOMZ-1B7'
#model='BLOOMZ-7B1'
#model='mGPT'
#model='mGPT-13B'
#model='xglm-1B7'
#model='xglm-7B5'

#en but ok multi
#model='Mistral-7B'
#model='Mistral-7B-Instruct'
#model='Llama-2-7B'
#model='Llama-2-7B-Chat'
#model='Llama-2-13B'
#model='Llama-2-13B-Chat'
#model='Gemma-2B'
#model='Gemma-2B-Instruct'
#model='Gemma-7B'
#model='Gemma-7B-Instruct'

#en
#model='Occiglot-7B'
# model='Occiglot-7B-Instruct'
#model='FLOR-1B3'
#model='FLOR-1B3-Instruct'
#model='FLOR-6B3'
#model='FLOR-6B3-Instruct'

#ca
model='FLOR-760M'
model='salamandra2b'
#model='FLOR-1B3'
#model='FLOR-1B3-Instruct'
#model='FLOR-6B3'
#model='FLOR-6B3-Instruct'

#es
#model='FLOR-1B3'
#model='FLOR-1B3-Instruct'
#model='FLOR-6B3'
#model='FLOR-6B3-Instruct'
#model='Occiglot-7B'
#model='Occiglot-7B-Instruct'

#it
#model='Occiglot-7B'
#model='Occiglot-7B-Instruct'

#de
#model='Occiglot-7B'
#model='Occiglot-7B-Instruct'

#eu
#model='Latxa-7B'

#gl
#model='FLOR-1B3-GL'
#model='Cerebras-1B3-GL'

#pt-br

#ko

#######################--TASKS--#######################

# CORE for all languages EXCEPT eu
# generate_all_hf_predictions(task_names=["sentence_containing","sentence_not_containing","word_containing","word_not_containing","most_associated_word","least_associated_word","any_words_from_category","all_words_from_category","first_alphabetically","more_letters","less_letters","bigger_number"], model_name=model)
# generate_all_hf_predictions(task_names=["smaller_number","rhyming_word","homophones","word_after","word_before","starts_with_word","ends_with_word","starts_with_letter","ends_with_letter","first_word","last_word","first_letter","last_letter"], model_name=model)

# CORE for eu ONLY
#generate_all_hf_predictions(task_names=["sentence_containing","sentence_not_containing","word_containing","word_not_containing","most_associated_word","least_associated_word","any_words_from_category","all_words_from_category","first_alphabetically","more_letters","less_letters","bigger_number"], model_name=model)
#generate_all_hf_predictions(task_names=["smaller_number","rhyming_word","word_after","word_before","starts_with_word","ends_with_word","starts_with_letter","ends_with_letter","first_word","last_word","first_letter","last_letter"], model_name=model)

# ANAL for all languages
# generate_all_hf_predictions(task_names=["first_alphabetically_far_first_letter","first_alphabetically_different_first_letter","first_alphabetically_consecutive_first_letter","first_alphabetically_same_first_letter","any_words_from_category_5_distractors","any_words_from_category_4_distractors","any_words_from_category_3_distractors","all_words_from_category_0_distractors"], model_name=model)
# generate_all_hf_predictions(task_names=["all_words_from_category_1_distractors","all_words_from_category_2_distractors","rhyming_word_orthographically_similar","more_letters_length_diff_3plus","more_letters_length_diff_1","less_letters_length_diff_3plus","less_letters_length_diff_1"], model_name=model)

# ANAL additional for en ONLY
#generate_all_hf_predictions(task_names=["rhyming_word_orthographically_different"], model_name=model)

# FIXES
# models=['BLOOM-7B1','BLOOMZ-1B7','BLOOMZ-7B1','mGPT','xglm-1B7']

# for model in models:
#     generate_all_hf_predictions(task_names=['homophones'], model_name=model)

#generate_all_hf_predictions(task_names=["first_alphabetically_far_first_letter"], model_name=model)
# generate_task_hf_predictions(task_name, model, model_name, max_length, batch_size)


def main(args):
    lang = args.language
    # for all languages EXCEPT eu and en
    # models=['BLOOM-7B1','BLOOMZ-1B7','BLOOMZ-7B1','mGPT','xglm-1B7']

    models = args.model_list
    
    print("#"*30)
    print("Testing the following models:\n", models)
    print("Testing the Language:", lang)
    print("#"*30)

    ## initialize the global variables
    initialize_variables(lang)
    
    from lmentry.predict import generate_all_hf_predictions


    for model in models:
        if lang == "eu":
            #for eu
            generate_all_hf_predictions(task_names=["sentence_containing","sentence_not_containing","word_containing","word_not_containing","most_associated_word","least_associated_word","any_words_from_category","all_words_from_category","first_alphabetically","more_letters","less_letters","bigger_number"], model_name=model)
            generate_all_hf_predictions(task_names=["smaller_number","rhyming_word","word_after","word_before","starts_with_word","ends_with_word","starts_with_letter","ends_with_letter","first_word","last_word","first_letter","last_letter"], model_name=model)
            generate_all_hf_predictions(task_names=["first_alphabetically_far_first_letter","first_alphabetically_different_first_letter","first_alphabetically_consecutive_first_letter","first_alphabetically_same_first_letter","any_words_from_category_5_distractors","any_words_from_category_4_distractors","any_words_from_category_3_distractors","all_words_from_category_0_distractors"], model_name=model)
            generate_all_hf_predictions(task_names=["all_words_from_category_1_distractors","all_words_from_category_2_distractors","rhyming_word_orthographically_similar","more_letters_length_diff_3plus","more_letters_length_diff_1","less_letters_length_diff_3plus","less_letters_length_diff_1"], model_name=model)
        elif lang == "en":
            # for en
            generate_all_hf_predictions(task_names=["sentence_containing","sentence_not_containing","word_containing","word_not_containing","most_associated_word","least_associated_word","any_words_from_category","all_words_from_category","first_alphabetically","more_letters","less_letters","bigger_number"], model_name=model)
            generate_all_hf_predictions(task_names=["smaller_number","rhyming_word","homophones","word_after","word_before","starts_with_word","ends_with_word","starts_with_letter","ends_with_letter","first_word","last_word","first_letter","last_letter"], model_name=model)
            generate_all_hf_predictions(task_names=["first_alphabetically_far_first_letter","first_alphabetically_different_first_letter","first_alphabetically_consecutive_first_letter","first_alphabetically_same_first_letter","any_words_from_category_5_distractors","any_words_from_category_4_distractors","any_words_from_category_3_distractors","all_words_from_category_0_distractors"], model_name=model)
            generate_all_hf_predictions(task_names=["all_words_from_category_1_distractors","all_words_from_category_2_distractors","rhyming_word_orthographically_similar","more_letters_length_diff_3plus","more_letters_length_diff_1","less_letters_length_diff_3plus","less_letters_length_diff_1"], model_name=model)
            generate_all_hf_predictions(task_names=["rhyming_word_orthographically_different"], model_name=model)
            generate_all_hf_predictions(task_names=["all_words_from_category_1_distractors","all_words_from_category_2_distractors","rhyming_word_orthographically_similar","more_letters_length_diff_3plus","more_letters_length_diff_1","less_letters_length_diff_3plus","less_letters_length_diff_1"], model_name=model)
        else:
            generate_all_hf_predictions(task_names=["sentence_containing","sentence_not_containing","word_containing","word_not_containing","most_associated_word","least_associated_word","any_words_from_category","all_words_from_category","first_alphabetically","more_letters","less_letters","bigger_number"], model_name=model)
            generate_all_hf_predictions(task_names=["smaller_number","rhyming_word","homophones","word_after","word_before","starts_with_word","ends_with_word","starts_with_letter","ends_with_letter","first_word","last_word","first_letter","last_letter"], model_name=model)
            generate_all_hf_predictions(task_names=["first_alphabetically_far_first_letter","first_alphabetically_different_first_letter","first_alphabetically_consecutive_first_letter","first_alphabetically_same_first_letter","any_words_from_category_5_distractors","any_words_from_category_4_distractors","any_words_from_category_3_distractors","all_words_from_category_0_distractors"], model_name=model)
            generate_all_hf_predictions(task_names=["all_words_from_category_1_distractors","all_words_from_category_2_distractors","rhyming_word_orthographically_similar","more_letters_length_diff_3plus","more_letters_length_diff_1","less_letters_length_diff_3plus","less_letters_length_diff_1"], model_name=model)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='Execute Prediction')
    parser.add_argument('-l', '--language', type=str, required=True)
    parser.add_argument('-m', '--model_list', nargs='+', required=True)
    args = parser.parse_args()
    main(args)