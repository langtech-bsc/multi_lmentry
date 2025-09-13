import re

from lmentry.scorers.ca.scorer import LMentryScorer, the_word_regex


class FirstAlphabeticallyScorer(LMentryScorer):
    def __init__(self):
        super().__init__()

        self.prefixes.extend([
            "Alfabèticament, ",
            "Seguint l'ordre alfabètic, ",
            "En ordre alfabètic, ",
            "De les paraules {word1} i {word2}, ",
        ])

        self.suffixes.extend([
            " alfabèticament",
            " seguint l'ordre alfabètic",
            " en ordre alfabètic",
            " al diccionari",
        ])

    def get_base_patterns(self, answer, distractor):

        comes = "(va|ve)"
        base_patterns = [
            rf"{answer} {comes} primer",
            rf"{distractor} {comes} segon",
            rf"{distractor} {comes} després",
            rf"{answer} {comes} abans de {distractor}",
            rf"{distractor} {comes} després de {answer}",
        ]
        return base_patterns + self.get_shared_patterns(target=answer)

    def get_exact_patterns(self, answer):
        return [
            rf"{answer}",
        ]

    def negative_scorer(self, prediction, answer):
        score, certainty = None, None

        predictions_words = re.findall(r"\b[a-z]+\b", prediction)
        if len(predictions_words) == 1 and predictions_words[0] != answer:
            score = 0
            certainty = 1

        return score, certainty

    def score_prediction(self, prediction, example, truncate_prediction: bool = False):
        prediction = self.normalize_prediction(prediction, truncate_prediction)

        metadata = example["metadata"]
        answer = metadata["answer"]
        score, certainty = self.negative_scorer(prediction, answer)
        if score is not None:
            return score, certainty

        distractor = metadata["distractor"]
        word1 = metadata["word1"]
        word2 = metadata["word2"]

        answer = the_word_regex(answer)
        distractor = the_word_regex(distractor)
        word1 = the_word_regex(word1)
        word2 = the_word_regex(word2)

        exact_patterns = self.get_exact_patterns(answer)
        for exact_pattern in exact_patterns:
            score, certainty = self._simple_scorer(prediction, answer=exact_pattern)
            if score:
                return score, certainty

        base_patterns = self.get_base_patterns(answer, distractor)
        self.prefix_kwargs = {"word1": word1, "word2": word2}

        score, certainty = self.certainty_scorer(prediction, base_patterns)
        return score, certainty
