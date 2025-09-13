import re

from lmentry.scorers.en.scorer import LMentryScorer, the_word_regex, the_letter_regex


class EndsWithLetterScorer(LMentryScorer):
    """This class was created by simply mirroring `StartsWithLetterScorer`
    """
    def __init__(self):
        super().__init__()

    def get_base_patterns(self, letter, word):

        word_ = r"(Antwort)"
        possible = r""
        a = r"(ein)"

        base_patterns = [
            rf"Ein mögliches Wort ist {word}",
            rf"Eine mögliche {word_} ist {word}",
            rf"{word} ist {a} mögliches Wort",
            rf"{word} endet auf {letter}",
            rf"{word} ist {a} Wort, das auf {letter} endet",
            rf"{word} ist {a} Wort, das mit {letter} aufhört",
            rf"{word} ist {a} Wort mit {letter} am Ende",
            rf"{word} ist {a} Wort, dessen letzter Buchstabe {letter} ist"
            rf"Wie wäre es mit {word}"
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
        word = the_word_regex(word)

        score, certainty = self._simple_scorer(prediction, word)
        if score:
            return score, certainty

        letter = the_letter_regex(letter)

        base_patterns = self.get_base_patterns(letter, word)

        score, certainty = self.certainty_scorer(prediction, base_patterns)
        return score, certainty
