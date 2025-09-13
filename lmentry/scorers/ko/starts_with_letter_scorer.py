import re

from lmentry.scorers.ko.scorer import LMentryScorer, the_word_regex, the_letter_regex


class StartsWithLetterScorer(LMentryScorer):
    def __init__(self):
        super().__init__()

    def get_base_patterns(self, letter, word):

        word_ = r"(단어|답)"
        possible = r"가능한"
        starts = r"(시작하는|시작함)"
        starting = r"(시작하는|시작함)"
        is_ = r"(이|가|은|는|와|과|의|에서|으|으로)"
        
        base_patterns = [
            rf"가능한 {word_}{is_} {word}입니다",
            rf"{word}{is_} 조건에 맞는 {word_}입니다",
            rf"{word}{is_} {letter}{is_} 시작합니다",
            rf"{word}{is_} {letter}{is_} 시작하는 단어입니다",
            rf"{letter}{is_} 시작하는 단어는 {word}입니다",
            rf"{word}{is_} 첫 글자가 {letter}인 단어입니다",
            rf"{word}{is_} 어떠세요?",
            rf"{word}{is_} 어떤가요?"
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

        after_the_letter = r"\w*" if letter in {"a", "i"} else r"\w+"

        word = rf"{letter}-?{after_the_letter}"  # the "-" is for cases like e-mail and x-ray
        word = the_word_regex(word)

        score, certainty = self._simple_scorer(prediction, word)
        if score:
            return score, certainty

        letter = the_letter_regex(letter)

        base_patterns = self.get_base_patterns(letter, word)

        score, certainty = self.certainty_scorer(prediction, base_patterns)
        return score, certainty
