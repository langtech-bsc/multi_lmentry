import re

from lmentry.scorers.pt_br.scorer import LMentryScorer, the_word_regex, the_letter_regex


class EndsWithLetterScorer(LMentryScorer):
    """This class was created by simply mirroring `StartsWithLetterScorer`
    """
    def __init__(self):
        super().__init__()

    def get_base_patterns(self, letter, word):

        word_ = r"(palavra|resposta)"
        possible = r"possível"
        a = r"uma"

        base_patterns = [
            rf"{a} {word_} {possible} é {word}",
            rf"{word} é {a} {word_} {possible}",
            rf"{word} termina com {letter}",
            rf"{word} termina com a letra {letter}",
            rf"{word} é {a} palavra que termina com {letter}",
            rf"{word} é {a} palavra que termina com a letra {letter}",
            rf"{word} é {a} palavra que acaba com {letter}",
            rf"{word} é {a} palavra que acaba com a letra {letter}",
            rf"{a} palavra que termina com {letter} é {word}",
            rf"{a} palavra que acaba com  {letter} é {word}",
            rf"{word} é {a} palavra cuja última letra é {letter}"
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

        valid_word = {"a", "o", "e"}
        before_the_letter = r"\w*" if letter in valid_word else r"\w+"

        word = rf"{before_the_letter}{letter}"
        word = the_word_regex(word)

        score, certainty = self._simple_scorer(prediction, word)
        if score:
            return score, certainty

        letter = the_letter_regex(letter)

        base_patterns = self.get_base_patterns(letter, word)

        score, certainty = self.certainty_scorer(prediction, base_patterns)
        return score, certainty
