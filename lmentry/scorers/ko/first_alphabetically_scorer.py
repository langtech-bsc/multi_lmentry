import re

from lmentry.scorers.ko.scorer import LMentryScorer, the_word_regex


class FirstAlphabeticallyScorer(LMentryScorer):
    def __init__(self):
        super().__init__()

        self.prefixes.extend([
            "가나다 순으로, ",
            "가나다 순으로 본다면, ",
            "가나다 순에서 볼 때, ",
            "{word1} 과 {word2} 중에서 ",
        ])

        self.suffixes.extend([
            " 가나다 순으로",
            " 가나다 순에서",
            " 사전에서",
        ])

    def get_base_patterns(self, answer, distractor):

        comes = "(comes|is)"
        is_ = r"(이|가|은|는|와|과|의|에서|을|를)"
        with_ = r"로|으로"
        base_patterns = [
            rf"{answer}{is_} 먼저 온다.",
            rf"{distractor}{is_} 두 번째로 온다.",
            rf"{distractor}{is_} 다음에 온다.",
            rf"{answer}{is_} {distractor} 전에 온다.",
            rf"{distractor}{is_} {answer} 다음에 온다.",
        ]
        return base_patterns + self.get_shared_patterns(target=answer)

    def get_exact_patterns(self, answer):
        return [
            rf"{answer}"
        ]

    def negative_scorer(self, prediction, answer):
        score, certainty = None, None

        predictions_words = re.findall(r"\b[a-z]+\b", prediction)
        if len(predictions_words) == 1 and predictions_words[0] != answer:
            score = 0
            certainty = 1

        return score, certainty

    def score_prediction(self, prediction, example, truncate_prediction: bool = False):
        prediction = self.normalize_prediction(prediction, truncate_prediction)

        metadata = example["metadata"]
        answer = metadata["answer"]
        score, certainty = self.negative_scorer(prediction, answer)
        if score is not None:
            return score, certainty

        distractor = metadata["distractor"]
        word1 = metadata["word1"]
        word2 = metadata["word2"]

        answer = the_word_regex(answer)
        distractor = the_word_regex(distractor)
        word1 = the_word_regex(word1)
        word2 = the_word_regex(word2)

        exact_patterns = self.get_exact_patterns(answer)
        for exact_pattern in exact_patterns:
            score, certainty = self._simple_scorer(prediction, answer=exact_pattern)
            if score:
                return score, certainty

        base_patterns = self.get_base_patterns(answer, distractor)
        self.prefix_kwargs = {"word1": word1, "word2": word2}

        score, certainty = self.certainty_scorer(prediction, base_patterns)
        return score, certainty
