import re

from lmentry.scorers.ko.scorer import LMentryScorer, the_word_regex, swap_substrings


class HomophoneScorer(LMentryScorer):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_exact_patterns(answer, query, distractor):

        _but = r"(\.,)? (하지만|그러나)"
        like = "(처럼|와 비슷하게)"
        is_ = r"(이|가|은|는|와|과|의|에서|을|를)"

        exact_patterns = [
            rf"{query}{is_} {answer}{like} 들립니다",
            rf"{query}{is_} {answer}{like} {_but} {distractor}처럼은 아닙니다",
            rf"{query}{is_} {answer}{like} 들리지만 {distractor}은(는) 그렇지 않습니다",
            rf"{query}{is_} {answer}는 비슷하게 들립니다",
            rf"{query}{is_} {distractor}보다 {answer}처럼 들립니다"            
        ]


        # swap answer and query
        more_exact_patterns = [
            swap_substrings(s, subs1=answer, subs2=query) for s in exact_patterns
        ]
        exact_patterns.extend(more_exact_patterns)

        return exact_patterns

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

        score, certainty = self.negative_scorer(prediction, answer)
        if score is not None:
            return score, certainty

        answer = the_word_regex(answer)

        score, certainty = self._simple_scorer(prediction, answer)
        if score:
            return score, certainty

        query = metadata["query"]
        distractor = metadata["distractor"]
        query = the_word_regex(query)
        distractor = the_word_regex(distractor)
        exact_patterns = self.get_exact_patterns(answer, query, distractor)

        for exact_pattern in exact_patterns:
            score, certainty = self._simple_scorer(prediction, exact_pattern)
            if score:
                return score, certainty
        else:
            score = 0
            certainty = 0

        return score, certainty
