import string

from lmentry.scorers.de.starts_with_letter_scorer import StartsWithLetterScorer
from lmentry.tasks.task import LMentryTask


class StartsWithLetter(LMentryTask):

    scorer_cls = StartsWithLetterScorer

    def __init__(self, name="starts_with_letter"):
        super().__init__(name)

        self.canonical_template = 'Schreibe ein Wort, das mit dem Buchstaben "{letter}" beginnt:'
        self.second_template = 'Schreibe ein Wort, dessen erster Buchstabe "{letter}" ist:'
        self.third_template = 'Schreibe ein Wort, das mit "{letter}" anfängt:'
        self.all_templates = [self.canonical_template, self.second_template, self.third_template]
        self.parameter_names = ["letter"]

    def _create_input(self, template, letter):
        input_ = template.format(letter=letter)
        return input_

    def create_data(self, task_data_path=None):

        # create examples
        examples = {}
        letters = string.ascii_lowercase
        de_letters = set(letters) | {"ß", "ä", "ö", "ü"}
        allowed_letters = set(de_letters) - {"ß", "c", "x", "y"}
        allowed_letters = sorted(allowed_letters)

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
