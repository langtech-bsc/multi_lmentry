from lmentry.scorers.ko.ends_with_letter_scorer import EndsWithLetterScorer
from lmentry.tasks.task import LMentryTask
from lmentry.ko_utils import FULL_ALPHABET

class EndsWithLetter(LMentryTask):

    scorer_cls = EndsWithLetterScorer

    def __init__(self, name="ends_with_letter"):
        super().__init__(name)

        self.canonical_template = '"{letter}"로 끝나는 단어를 작성하시오:'
        self.second_template = '마지막 글자가 "{letter}"인 단어를 작성하시오:'
        self.third_template = '"{letter}"로 끝나는 단어를 작성하시오:'
        self.all_templates = [self.canonical_template, self.second_template, self.third_template]
        self.parameter_names = ["letter"]

    def _create_input(self, template, letter):
        input_ = template.format(letter=letter)
        return input_

    def create_data(self, task_data_path=None):

        # create examples
        examples = {}

        allowed_letters = FULL_ALPHABET

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
        settings["num_examples_per_template"] = int(len(examples) / len(self.all_templates))
        settings["input_templates"] = self.all_templates

        # build the task_data
        task_data = dict()
        task_data["settings"] = settings
        task_data["examples"] = examples

        # save the data
        self.save_task_data(task_data)


if __name__ == '__main__':
    task = EndsWithLetter()
