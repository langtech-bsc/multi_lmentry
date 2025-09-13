import re

from lmentry.scorers.ca.scorer import LMentryScorer, the_sentence_regex, the_word_regex


class FirstWordScorer(LMentryScorer):
    def __init__(self):
        super().__init__()

        self.prefixes.extend([
            "A {sentence} ",
        ])

        self.suffixes.extend([
            " (de|a) {sentence}",
        ])

    def get_base_patterns(self, answer, sentence):

        base_patterns = [
            rf"La primera paraula és {answer}",
            rf"La primera paraula (de|a) {sentence} és {answer}",
            rf"{answer} és la primera paraula",
            rf"{sentence} comença amb {answer}",
            rf"Primera paraula: {answer}",
        ]

        return base_patterns + self.get_shared_patterns(target=answer)

    def negative_scorer(self, prediction, answer):
        score, certainty = None, None

        if not re.search(rf"\b{answer}\b", prediction):
            score = 0
            certainty = 1

        return score, certainty

    def score_prediction(self, prediction, example, truncate_prediction: bool = False):
        prediction = self.normalize_prediction(prediction, truncate_prediction)

        metadata = example["metadata"]
        answer = metadata["answer"]
        sentence = metadata["sentence"]

        # in the first/last word tasks, the sentence and the answer are saved in their original case
        # as many sentence words are named entities. in scoring, we choose to ignore the case.
        answer = answer.lower()
        sentence = sentence.lower()
        
        score, certainty = self.negative_scorer(prediction, answer)
        if score is not None:
            return score, certainty

        answer = the_word_regex(answer)
        sentence = the_sentence_regex(sentence)

        score, certainty = self._simple_scorer(prediction, answer)
        if score:
            return score, certainty

        base_patterns = self.get_base_patterns(answer, sentence)
        self.prefix_kwargs = {"sentence": sentence}
        self.suffix_kwargs = {"sentence": sentence}

        score, certainty = self.certainty_scorer(prediction, base_patterns)
        return score, certainty
