import string

from lmentry.scorers.pt_br.word_not_containing_scorer import WordNotContainingScorer
from lmentry.tasks.task import LMentryTask


class WordNotContaining(LMentryTask):

    scorer_cls = WordNotContainingScorer

    def __init__(self, name="word_not_containing"):
        super().__init__(name)
        self.canonical_template = 'Escreva uma palavra que não contenha a letra "{letter}":'
        self.second_template = 'Escreva uma palavra sem usar a letra "{letter}":'
        self.third_template = 'Escreva uma palavra sem a letra "{letter}":'
        self.all_templates = [self.canonical_template, self.second_template, self.third_template]
        self.parameter_names = ["letter"]

    def _create_input(self, template, letter):
        input_ = template.format(letter=letter)
        return input_

    def create_data(self, task_data_path=None):

        # create examples
        examples = {}

        for template_id, template in enumerate(self.all_templates):
            letters = string.ascii_lowercase
            es_letters = set(letters) | {"ç"}
            for letter in es_letters:
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
        settings["num_examples_per_template"] = len(es_letters)
        settings["input_templates"] = self.all_templates

        # build the task_data
        task_data = dict()
        task_data["settings"] = settings
        task_data["examples"] = examples

        # save the data
        self.save_task_data(task_data)


if __name__ == '__main__':
    task = WordNotContaining()
