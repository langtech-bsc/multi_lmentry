from lmentry.constants import initialize_variables
import argparse

def main(args):
    lang = args.language
    # for all languages EXCEPT eu and en
    # models=['BLOOM-7B1','BLOOMZ-1B7','BLOOMZ-7B1','mGPT','xglm-1B7']

    models = args.model_list
    use_vllm = args.use_vllm
    
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
            generate_all_hf_predictions(task_names=["sentence_containing","sentence_not_containing","word_containing","word_not_containing","most_associated_word","least_associated_word","any_words_from_category","all_words_from_category","first_alphabetically","more_letters","less_letters","bigger_number"], model_name=model, use_vllm=use_vllm)
            generate_all_hf_predictions(task_names=["smaller_number","rhyming_word","word_after","word_before","starts_with_word","ends_with_word","starts_with_letter","ends_with_letter","first_word","last_word","first_letter","last_letter"], model_name=model, use_vllm=use_vllm)
            generate_all_hf_predictions(task_names=["first_alphabetically_far_first_letter","first_alphabetically_different_first_letter","first_alphabetically_consecutive_first_letter","first_alphabetically_same_first_letter","any_words_from_category_5_distractors","any_words_from_category_4_distractors","any_words_from_category_3_distractors","all_words_from_category_0_distractors"], model_name=model, use_vllm=use_vllm)
            generate_all_hf_predictions(task_names=["all_words_from_category_1_distractors","all_words_from_category_2_distractors","rhyming_word_orthographically_similar","more_letters_length_diff_3plus","more_letters_length_diff_1","less_letters_length_diff_3plus","less_letters_length_diff_1"], model_name=model, use_vllm=use_vllm)
        elif lang == "en":
            # for en
            generate_all_hf_predictions(task_names=["sentence_containing","sentence_not_containing","word_containing","word_not_containing","most_associated_word","least_associated_word","any_words_from_category","all_words_from_category","first_alphabetically","more_letters","less_letters","bigger_number"], model_name=model, use_vllm=use_vllm)
            generate_all_hf_predictions(task_names=["smaller_number","rhyming_word","homophones","word_after","word_before","starts_with_word","ends_with_word","starts_with_letter","ends_with_letter","first_word","last_word","first_letter","last_letter"], model_name=model, use_vllm=use_vllm)
            generate_all_hf_predictions(task_names=["first_alphabetically_far_first_letter","first_alphabetically_different_first_letter","first_alphabetically_consecutive_first_letter","first_alphabetically_same_first_letter","any_words_from_category_5_distractors","any_words_from_category_4_distractors","any_words_from_category_3_distractors","all_words_from_category_0_distractors"], model_name=model, use_vllm=use_vllm)
            generate_all_hf_predictions(task_names=["all_words_from_category_1_distractors","all_words_from_category_2_distractors","rhyming_word_orthographically_similar","more_letters_length_diff_3plus","more_letters_length_diff_1","less_letters_length_diff_3plus","less_letters_length_diff_1"], model_name=model, use_vllm=use_vllm)
            generate_all_hf_predictions(task_names=["rhyming_word_orthographically_different"], model_name=model, use_vllm=use_vllm)
            generate_all_hf_predictions(task_names=["all_words_from_category_1_distractors","all_words_from_category_2_distractors","rhyming_word_orthographically_similar","more_letters_length_diff_3plus","more_letters_length_diff_1","less_letters_length_diff_3plus","less_letters_length_diff_1"], model_name=model, use_vllm=use_vllm)
        else:
            generate_all_hf_predictions(task_names=["sentence_containing","sentence_not_containing","word_containing","word_not_containing","most_associated_word","least_associated_word","any_words_from_category","all_words_from_category","first_alphabetically","more_letters","less_letters","bigger_number"], model_name=model, use_vllm=use_vllm)
            generate_all_hf_predictions(task_names=["smaller_number","rhyming_word","homophones","word_after","word_before","starts_with_word","ends_with_word","starts_with_letter","ends_with_letter","first_word","last_word","first_letter","last_letter"], model_name=model, use_vllm=use_vllm)
            generate_all_hf_predictions(task_names=["first_alphabetically_far_first_letter","first_alphabetically_different_first_letter","first_alphabetically_consecutive_first_letter","first_alphabetically_same_first_letter","any_words_from_category_5_distractors","any_words_from_category_4_distractors","any_words_from_category_3_distractors","all_words_from_category_0_distractors"], model_name=model, use_vllm=use_vllm)
            generate_all_hf_predictions(task_names=["all_words_from_category_1_distractors","all_words_from_category_2_distractors","rhyming_word_orthographically_similar","more_letters_length_diff_3plus","more_letters_length_diff_1","less_letters_length_diff_3plus","less_letters_length_diff_1"], model_name=model, use_vllm=use_vllm)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='Execute Prediction')
    parser.add_argument('-l', '--language', type=str, required=True)
    parser.add_argument('-m', '--model_list', nargs='+', required=True)
    parser.add_argument('-v', '--use_vllm', action="store_true")
    args = parser.parse_args()
    main(args)