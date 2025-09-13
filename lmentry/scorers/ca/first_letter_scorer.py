import re

from lmentry.scorers.ca.scorer import LMentryScorer, the_word_regex, the_letter_regex


class FirstLetterScorer(LMentryScorer):
    def __init__(self):
        super().__init__()

    def get_base_patterns(self, answer, word):

        of = "(de|a)"
        starts = "(comença)"

        base_patterns = [
            rf"La primera lletra és {answer}",
            rf"La primera lletra {of} {word} és {answer}",
            rf"{answer} és la primera lletra {of} {word}",
            rf"{word} {starts} amb {answer}",
            rf"La lletra amb què {starts} {word} és {answer}",
            rf"{answer} és la lletra inicial {of} {word}",
            rf"{word}: {answer}",
            rf"Primera lletra: {answer}",
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
