import re

from lmentry.scorers.ko.scorer import LMentryScorer, the_word_regex, the_letter_regex


class EndsWithLetterScorer(LMentryScorer):
    """This class was created by simply mirroring `StartsWithLetterScorer`
    """
    def __init__(self):
        super().__init__()

    def get_base_patterns(self, letter, word):

        word_ = r"(단어는|답은)"
        possible = r"(가능한|조건에 맞는)"
        is_ = r"(이|가|은|는|와|과|의|에서|을|를)"
        with_ = r"로|으로"
        
        base_patterns = [
            rf"{possible} {word_} {word}이다",
            rf"{word}{is_} {possible} {word_}",
            rf"{word}{is_} {letter}로 끝난다",
            rf"{word}{is_} {letter}로 끝나는 단어이다."
            rf"{word}{is_} {letter}로 끝나는 답이다.",
            rf"{letter}{with_} 끝나는 단어는 {word}이다.",
            rf"{word} 어떤가요?",
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

        before_the_letter = r"\w*" if letter in {"a", "i"} else r"\w+"

        word = rf"{before_the_letter}{letter}"
        word = the_word_regex(word)

        score, certainty = self._simple_scorer(prediction, word)
        if score:
            return score, certainty

        letter = the_letter_regex(letter)

        base_patterns = self.get_base_patterns(letter, word)

        score, certainty = self.certainty_scorer(prediction, base_patterns)
        return score, certainty
