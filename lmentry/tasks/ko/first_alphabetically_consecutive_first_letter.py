import json
import random
from collections import defaultdict

from lmentry.constants import LMENTRY_WORDS_PATH
from lmentry.scorers.ko.first_alphabetically_scorer import FirstAlphabeticallyScorer
from lmentry.tasks.task import LMentryTask

from lmentry.ko_utils import hangul_word_to_letters, FULL_ALPHABET

class FirstAlphabeticallyConsecutiveFirstLetter(LMentryTask):

    scorer_cls = FirstAlphabeticallyScorer

    def __init__(self, name="first_alphabetically_consecutive_first_letter", words_path=None):
        super().__init__(name)
        self.canonical_template = '가나다 순서로 했을 때, 먼저 오는 단어는 "{word1}"과 "{word2}" 중 무엇입니까?'
        self.second_template = '가나다 순으로 했을 때, "{word1}"과 "{word2}" 중 어느 단어가 더 먼저입니까?'
        self.third_template = '단어 "{word1}"과 "{word2}" 중 가나다 순으로 했을 때, 더 먼저 오는 단어는 무엇입니까?'
        self.all_templates = [self.canonical_template, self.second_template, self.third_template]
        self.parameter_names = ["answer", "distractor"]
        self.words_path = words_path or LMENTRY_WORDS_PATH

    def _create_input(self, answer: str, distractor: str, answer_index: int, template):

        if answer_index == 0:
            word1 = answer
            word2 = distractor
        elif answer_index == 1:
            word1 = distractor
            word2 = answer

        input_ = template.format(word1=word1, word2=word2)

        return input_

    def create_data(self, num_examples=1000, seed=None, task_data_path=None):

        # get a dict of (<first letter>: <list of words word>) for all words
        with open(self.words_path) as f_words:
            words_data = json.load(f_words)

        words = []

        for word, _ in words_data.items():
            words.append(word)

        first_letter_to_words = defaultdict(list)
        for word in words:
            first_letter = hangul_word_to_letters(word)[0]
            first_letter_to_words[first_letter].append(word)

        all_letters = FULL_ALPHABET
        all_answer_first_letter_options = [
            c for c in all_letters
            if c in first_letter_to_words
            and chr(ord(c)+1) in first_letter_to_words
        ]

        # create examples
        examples = dict()
        for template_id, template in enumerate(self.all_templates):

            seed = seed or self.default_seed
            random.seed(seed)
            num_template_examples_created = 0
            already_seen_arguments: set[tuple[str, str, int]] = set()  # answer, distractor, answer_index

            while num_template_examples_created < num_examples:
                answer_first_letter = random.choice(all_answer_first_letter_options)
                answer = random.choice(first_letter_to_words[answer_first_letter])

                distractor_first_letter = chr(ord(answer_first_letter) + 1)
                distractor = random.choice(first_letter_to_words[distractor_first_letter])

                answer_index = random.choice((0, 1))

                if (answer, distractor, answer_index) in already_seen_arguments:
                    continue
                already_seen_arguments.add((answer, distractor, answer_index))

                input_ = self._create_input(answer, distractor, answer_index, template)

                # create the metadata
                metadata = dict()
                metadata["answer"] = answer
                metadata["distractor"] = distractor
                metadata["answer_index"] = answer_index
                metadata["word1"] = answer if answer_index == 0 else distractor
                metadata["word2"] = answer if answer_index == 1 else distractor
                metadata["template_id"] = template_id

                # create the example
                example = dict()
                example["input"] = input_
                example["metadata"] = metadata
                examples[str(len(examples) + 1)] = example

                num_template_examples_created += 1

        # create the shared settings
        settings = dict()
        settings["canary"] = self.canary_string
        settings["name"] = self.name
        settings["num_examples_per_template"] = num_examples
        settings["seed"] = seed
        settings["input_templates"] = self.all_templates

        # build the task_data
        task_data = dict()
        task_data["settings"] = settings
        task_data["examples"] = examples

        # save the data
        self.save_task_data(task_data)


if __name__ == '__main__':
    task = FirstAlphabeticallyConsecutiveFirstLetter()
