import re

from lmentry.scorers.ko.scorer import LMentryScorer, the_word_regex, the_letter_regex


class FirstLetterScorer(LMentryScorer):
    def __init__(self):
        super().__init__()

    def get_base_patterns(self, answer, word):
        is_ = r"(이|가|은|는)"
        with_ = r"로|으로"
        
        base_patterns = [
            rf"첫 번째 글자는 {answer}입니다.",
            rf"{word}의 첫 번째 글자는 {answer}입니다.",
            rf"{answer}{is_} {word}의 첫 글자입니다.",
            rf"{word}{is_} {answer}로 시작합니다.",
            rf"{word}{is_} 시작하는 글자는 {answer}입니다."
            rf"{answer}{is_} {word}의 시작 글자입니다.",
            rf"{word}: {answer}",
            rf"첫 글자: {answer}"
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
        word = metadata["word"]

        score, certainty = self.negative_scorer(prediction, answer)
        if score is not None:
            return score, certainty

        answer = the_letter_regex(answer)

        score, certainty = self._simple_scorer(prediction, answer)
        if score:
            return score, certainty

        word = the_word_regex(word)

        base_patterns = self.get_base_patterns(answer, word)

        score, certainty = self.certainty_scorer(prediction, base_patterns)
        return score, certainty
