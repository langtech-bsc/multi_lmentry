import re

from lmentry.scorers.ca.scorer import LMentryScorer, the_word_regex, the_letter_regex


class EndsWithLetterScorer(LMentryScorer):
    """This class was created by simply mirroring `StartsWithLetterScorer`
    """
    def __init__(self):
        super().__init__()

    def get_base_patterns(self, letter, word):

        word_ = r"(paraula|resposta)"
        possible = r"possible"
        a = r"(una)"

        base_patterns = [
            rf"{a} {possible} {word_} és {word}",
            rf"{word} és {a} {possible} {word_}",
            rf"{word} acaba amb {letter}",
            rf"{word} és {a} paraula que acaba amb la lletra {letter}",
            rf"{word} és {a} paraula acabada en {letter}",
            rf"{a} paraula acabada en {letter} és {word}",
            rf"{a} paraula acabada amb la lletra {letter} és {word}",
            rf"{word} és {a} paraula l'última lletra de la qual és {letter}",
        ]
        return base_patterns + self.get_shared_patterns(target=word)

    def negative_scorer(self, prediction, letter):
        score, certainty = None, None

        prediction_words = re.findall(r"\b[a-z]+\b", prediction)

        if all([word[-1] != letter for word in prediction_words]):
            score = 0
            certainty = 1

        return score, certainty

    def score_prediction(self, prediction, example, truncate_prediction: bool = False):
        prediction = self.normalize_prediction(prediction, truncate_prediction)

        letter = example["metadata"]["letter"]

        score, certainty = self.negative_scorer(prediction, letter)
        if score is not None:
            return score, certainty

        before_the_letter = r"\w*" if letter in {"a", "i", "o"} else r"\w+" #Allow single letter words

        word = rf"{before_the_letter}{letter}"
        word = the_word_regex(word)

        score, certainty = self._simple_scorer(prediction, word)
        if score:
            return score, certainty

        letter = the_letter_regex(letter)

        base_patterns = self.get_base_patterns(letter, word)

        score, certainty = self.certainty_scorer(prediction, base_patterns)
        return score, certainty
