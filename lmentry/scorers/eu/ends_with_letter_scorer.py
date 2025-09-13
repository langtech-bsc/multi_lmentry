import re

from lmentry.eu_declension import instrumental_singular, comitative_singular
from lmentry.scorers.eu.scorer import LMentryScorer, the_word_regex


class EndsWithLetterScorer(LMentryScorer):
    """This class was created by simply mirroring `StartsWithLetterScorer`
    """
    def __init__(self):
        super().__init__()

    # 'Idatzi "{letter}" letrarekin amaitzen den hitz bat:\n'
    # 'idatzi hitz bat zeinen azken letra "{letter}" den:\n'
    # 'Idatzi hitz bat "{letter}" letrarekin amaituz:\n'

    def get_base_patterns(self, letter, word):

        letter = rf"\"?{letter}\"?"
        word = rf"\"?{word}\"?"

        with_letter = fr"({letter} {instrumental_singular('letra')}|{letter} {comitative_singular('letra')})"
        a_word = r"(hitza|hitz bat)"
        finishing = r"(amaitzen|bukatzen)"

        base_patterns = [
            rf"{with_letter} {finishing} den {a_word} {word} (da|izan daiteke)",
            rf"{with_letter} {finishing} den {a_word} da {word}",
            rf"{word}( hitza)? {with_letter} {finishing}( den {a_word})? da",
            fr"{with_letter} {finishing} den {a_word}: {word}",
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

        before_the_letter = r"\w+"

        word = rf"{before_the_letter}{letter}"

        score, certainty = self._simple_scorer(prediction, the_word_regex(word))
        if score:
            return score, certainty

        base_patterns = self.get_base_patterns(letter, word)

        score, certainty = self.certainty_scorer(prediction, base_patterns)
        return score, certainty
