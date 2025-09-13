import re

from lmentry.scorers.eu.scorer import LMentryScorer, swap_substrings, the_number_regex


class BiggerNumberScorer(LMentryScorer):

    def __init__(self):
        super().__init__()

        # "Q: Zein zenbaki da handiena, {n1} edo {n2}?\nA:"
        # "Q: {n1} eta {n2} zenbakien artean, zein da handiena?\nA:"
        # "{n1} eta {n2} zenbakien artean, aukeratu handiena:\nA:"

        self.prefixes.extend([
            r"{n1} eta {n2} zenbakien artean,? ",
            r"Zenbaki horien artean,? "
        ])

    def get_base_patterns(self, answer, distractor):

        bigger = r"handiagoa"
        biggest = r"handiena"

        base_patterns = [
            rf"{answer} ({bigger}|{biggest}) da",
            rf"{answer} da ({bigger}|{biggest})",
            rf"{answer} zenbaki(rik)? {biggest} da",
            rf"{answer} da zenbaki(rik)? {biggest}",
            rf"{answer} {distractor} baino {bigger} da",
            rf"{answer} {bigger} da {distractor} baino",
            rf"{biggest} {answer} da",
            rf"Zenbaki(rik)? {biggest} {answer} da",
        ]
        # replace bigger with smaller and swap answer and distractor
        more_base_patterns = [
            swap_substrings(s, subs1=answer, subs2=distractor).replace(bigger, "txikiagoa").replace(biggest, "txikiena")
            for s in base_patterns
        ]
        base_patterns.extend(more_base_patterns)

        return base_patterns + self.get_shared_patterns(target=answer)

    def negative_scorer(self, prediction, answer):
        score, certainty = None, None

        alphanumeric_pattern = r"\b[a-z\d]+\b"
        all_alphanumeric_words = re.findall(alphanumeric_pattern, prediction)

        if len(set(all_alphanumeric_words)) == 1:
            answer = str(answer)
            if all_alphanumeric_words[0] != answer:
                score = 0
                certainty = 1

        return score, certainty

    def score_prediction(self, prediction, example, truncate_prediction: bool = False):
        prediction = self.normalize_prediction(prediction, truncate_prediction)

        metadata = example["metadata"]
        n1 = metadata["n1"]
        n2 = metadata["n2"]
        answer = metadata["answer"]

        score, certainty = self.negative_scorer(prediction, answer)
        if score is not None:
            return score, certainty

        distractor = metadata["distractor"]

        answer = the_number_regex(answer)
        distractor = the_number_regex(distractor)

        score, certainty = self._simple_scorer(prediction, answer)
        if score:
            return score, certainty

        base_patterns = self.get_base_patterns(answer, distractor)
        self.prefix_kwargs = {"n1": n1, "n2": n2}

        score, certainty = self.certainty_scorer(prediction, base_patterns)
        return score, certainty
