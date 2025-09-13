import random

from lmentry.scorers.ca.bigger_number_scorer import BiggerNumberScorer
from lmentry.tasks.task import LMentryTask


class BiggerNumber(LMentryTask):

    scorer_cls = BiggerNumberScorer

    def __init__(self, name="bigger_number"):
        super().__init__(name)
        self.canonical_template = "Quin nombre és més gran: {n1} o {n2}?"
        self.second_template = "D'entre els nombres {n1} i {n2}, quin és més gran?"
        self.third_template = "D'entre els nombres {n1} i {n2}, escriu el nombre més gran:"
        self.all_templates = [self.canonical_template, self.second_template, self.third_template]
        self.parameter_names = ["answer", "distractor"]

    def _create_input(self, template, n1, n2):
        input_ = template.format(n1=str(n1), n2=str(n2))
        return input_

    def create_data(self, num_examples=1000, seed=None, task_data_path=None):

        examples = {}
        numbers_range = range(10, 1000)

        for template_id, template in enumerate(self.all_templates):
            # set random seed
            seed = seed or self.default_seed
            random.seed(seed)
            num_examples_created = 0
            already_sampled = []

            # create examples
            while num_examples_created < num_examples:
                # create the input
                # samples two different numbers
                numbers = random.sample(numbers_range, 2)
                if numbers in already_sampled:
                    continue
                already_sampled.append(numbers)
                num_examples_created += 1

                input_ = self._create_input(template, n1=numbers[0], n2=numbers[1])
                max_val = max(numbers[0], numbers[1])

                # create the metadata
                metadata = dict()
                metadata["num_digits"] = [len(str(numbers[0])), len(str(numbers[1]))]
                metadata["n1"] = numbers[0]
                metadata["n2"] = numbers[1]
                metadata["answer"] = max_val
                metadata["answer_index"] = numbers.index(max_val)
                metadata["distractor"] = metadata["n2"] if metadata["answer_index"] == 0 else metadata["n1"]
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
    task = BiggerNumber()
