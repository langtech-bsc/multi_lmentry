import re

from lmentry.scorers.en.scorer import LMentryScorer, the_word_regex, the_letter_regex


class StartsWithLetterScorer(LMentryScorer):
    def __init__(self):
        super().__init__()

    def get_base_patterns(self, letter, word):

        word_ = r"(Wort)"
        possible = r"mögliches"
        starts = r"(beginnt)"
        a = r"(ein)"

        base_patterns = [
            rf"{a} {possible} {word_} ist {word}",
            rf"{word} ist {a} {possible} {word_}",
            rf"{word} {starts} mit {letter}",
            rf"{word} ist {a} Wort, das mit {letter} {starts} ",
            rf"{word} ist {a} Wort, dessen erster Buchstabe {letter} ist",
            rf"Wie wäre es mit dem Wort {word}",
        ]
        return base_patterns + self.get_shared_patterns(target=word)

    def negative_scorer(self, prediction, letter):
        score, certainty = None, None

        prediction_words = re.findall(r"\b[a-z]+\b", prediction)

        if all([word[0] != letter for word in prediction_words]):
            score = 0
            certainty = 1

        return score, certainty

    def score_prediction(self, prediction, example, truncate_prediction: bool = False):
        prediction = self.normalize_prediction(prediction, truncate_prediction)

        letter = example["metadata"]["letter"]

        score, certainty = self.negative_scorer(prediction, letter)
        if score is not None:
            return score, certainty

        after_the_letter = r"\w+"

        word = rf"{letter}-?{after_the_letter}"  # the "-" is for cases like e-mail and x-ray
        word = the_word_regex(word)

        score, certainty = self._simple_scorer(prediction, word)
        if score:
            return score, certainty

        letter = the_letter_regex(letter)

        base_patterns = self.get_base_patterns(letter, word)

        score, certainty = self.certainty_scorer(prediction, base_patterns)
        return score, certainty
