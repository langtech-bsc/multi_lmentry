import re

from lmentry.eu_declension import *
from lmentry.scorers.eu.scorer import LMentryScorer, the_letter_regex


class LastLetterScorer(LMentryScorer):
    """This class was created by simply mirroring `FirstLetterScorer`
    """
    def __init__(self):
        super().__init__()

        # 'Q: Zein da "{word}" hitzaren azken letra?\nA:'
        # 'Q: Zein letrarekin amaitzen da "{word}" hitza?\nA:'
        # 'Idatzi "{word}" hitzaren azken letra:\n'

    def get_base_patterns(self, answer, word):

        answer = rf"\"?{answer}\"?"
        word = rf"\"?{word}\"?"

        last = r"(azken|azkenengo|amaierako|bukaerako)"
        ending = r"(amaiera|bukaera)"
        finish = r"(amaitzen|bukatzen)"
        with_answer = rf"{answer} ({comitative_singular('letra')}|{instrumental_singular('letra')})"
        of_word = rf"{word} ({possessive_genitive_singular('hitz')}|{local_genitive_singular('hitz')})"

        base_patterns = [
            with_answer,
            fr"{with_answer} {finish} da",
            fr"{word} {with_answer} {finish} da",
            fr"{word} hitza {with_answer} {finish} da",
            rf"{last} letra {answer} da",
            rf"{answer} da {last} letra",
            rf"{of_word} {last} letra {answer} da",
            rf"{of_word} {ending} {answer} da",
            rf"{answer} da {of_word} {last} letra",
            rf"{answer} da {of_word} {ending}",
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

        score, certainty = self._simple_scorer(prediction, the_letter_regex(answer))
        if score:
            return score, certainty

        base_patterns = self.get_base_patterns(answer, word)

        score, certainty = self.certainty_scorer(prediction, base_patterns)
        return score, certainty
