import re

from lmentry.scorers.es.scorer import LMentryScorer, the_word_regex, the_letter_regex


class LastLetterScorer(LMentryScorer):
    """This class was created by simply mirroring `FirstLetterScorer`
    """
    def __init__(self):
        super().__init__()

    def get_base_patterns(self, answer, word):

        of = "(de|en)"
        ends = "(acaba|termina)"

        base_patterns = [
            rf"La última letra es {answer}",
            rf"La última letra {of} {word} es {answer}",
            rf"{answer} es la última letra {of} {word}",
            rf"{word} {ends} con {answer}",
            rf"La letra con la que {word} {ends} es {answer}",
            rf"{answer} es la letra final {of} {word}",
            rf"{word}: {answer}",
            rf"Última letra: {answer}",
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
