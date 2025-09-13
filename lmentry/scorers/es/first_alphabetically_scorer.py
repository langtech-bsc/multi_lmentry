import re

from lmentry.scorers.es.scorer import LMentryScorer, the_word_regex


class FirstAlphabeticallyScorer(LMentryScorer):
    def __init__(self):
        super().__init__()

        self.prefixes.extend([
            "Alfabéticamente, ",
            "Siguiendo el orden alfabético, ",
            "En orden alfabético, ",
            "Entre las palabras {word1} y {word2}, ",
            "De las palabras {word1} y {word2}, ",
        ])

        self.suffixes.extend([
            " alfabéticamente",
            " siguiendo el orden alfabético",
            " en orden alfabético",
            " en el diccionario",
        ])

    def get_base_patterns(self, answer, distractor):

        comes = "(viene|va)"
        base_patterns = [
            rf"{answer} {comes} primero",
            rf"{distractor} {comes} segundo",
            rf"{distractor} {comes} después",
            rf"{answer} {comes} antes que {distractor}",
            rf"{distractor} {comes} después de {answer}",
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
