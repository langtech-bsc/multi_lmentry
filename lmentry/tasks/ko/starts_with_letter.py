import string

from lmentry.scorers.ko.starts_with_letter_scorer import StartsWithLetterScorer
from lmentry.tasks.task import LMentryTask
from lmentry.ko_utils import BASIC_CONSONANTS, TENSE_CONSONANTS

class StartsWithLetter(LMentryTask):

    scorer_cls = StartsWithLetterScorer

    def __init__(self, name="starts_with_letter"):
        super().__init__(name)

        self.canonical_template = '시작하는 글자가 "{letter}"인 단어를 작성하시오:'
        self.second_template = '첫 글자가 "{letter}"인 단어를 작성하시오:'
        self.third_template = '"{letter}"로 시작하는 단어를 작성하시오:'
        self.all_templates = [self.canonical_template, self.second_template, self.third_template]
        self.parameter_names = ["letter"]

    def _create_input(self, template, letter):
        input_ = template.format(letter=letter)
        return input_

    def create_data(self, task_data_path=None):

        # create examples
        examples = {}

        allowed_letters = BASIC_CONSONANTS | TENSE_CONSONANTS # words in Hangul only start with consonants

        for template_id, template in enumerate(self.all_templates):
            for letter in allowed_letters:
                # create the input
                input_ = self._create_input(template, letter)

                # create the metadata
                metadata = dict()
                metadata["letter"] = letter
                metadata["template_id"] = template_id

                # create the example
                example = dict()
                example["input"] = input_
                example["metadata"] = metadata
                examples[str(len(examples) + 1)] = example

        # create the shared settings
        settings = dict()
        settings["canary"] = self.canary_string
        settings["name"] = self.name
        settings["num_examples_per_template"] = len(string.ascii_lowercase)
        settings["input_templates"] = self.all_templates

        # build the task_data
        task_data = dict()
        task_data["settings"] = settings
        task_data["examples"] = examples

        # save the data
        self.save_task_data(task_data)


if __name__ == '__main__':
    task = StartsWithLetter()
