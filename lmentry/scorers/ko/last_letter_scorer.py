import re

from lmentry.scorers.ko.scorer import LMentryScorer, the_word_regex, the_letter_regex


class LastLetterScorer(LMentryScorer):
    """This class was created by simply mirroring `FirstLetterScorer`
    """
    def __init__(self):
        super().__init__()

    def get_base_patterns(self, answer, word):

        of = r"(이|가|은|는|와|과|의|에서|을|를)"
        
        base_patterns = [
            rf"마지막 글자는 {answer}입니다",
            rf"{word}{of} 마지막 글자는 {answer}입니다",
            rf"{answer}은(는) {word}{of} 마지막 글자입니다",
            rf"{word}는 {answer}(으)로 끝납니다",
            rf"{answer}은(는) {word}{of} 마지막 글자입니다",
            rf"{word}: {answer}",
            rf"마지막 글자: {answer}",
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
