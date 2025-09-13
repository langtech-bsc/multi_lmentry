import re

from lmentry.scorers.ca.scorer import LMentryScorer, the_word_regex, swap_substrings


class RhymingWordScorer(LMentryScorer):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_exact_patterns(answer, query, distractor):

        a = r"(una|la)"
        while_ = "(mentre que|però|i)"
        exact_patterns = [
            rf"{query} rima amb {answer}( i no amb {distractor})?",
            rf"{query} és {a} rima de {answer}( i no de {distractor})?",
            rf"{query} i {answer} riman",
            rf"{query} i {answer} són paraules que rimen",
            rf"{a} rima de {query} és {answer}( i no {distractor})?",
            rf"{a} paraula que rima amb {query} és {answer}",
            rf"{query} i {answer} rimen, {while_} {distractor} no rima amb cap d'elles"
        ]

        # swap answer and query
        more_exact_patterns = [
            swap_substrings(s, subs1=answer, subs2=query) for s in exact_patterns
        ]
        exact_patterns.extend(more_exact_patterns)

        more_exact_patterns_2 = [
            rf"{distractor} no rima amb {query}(\s+{answer} rima amb {query})?",
            rf"{query} no rima amb {distractor}(\s+{query} rima amb {answer})?",
            rf"{answer} rima amb {query}\s+{distractor} no rima amb {query}",
        ]
        exact_patterns.extend(more_exact_patterns_2)

        return exact_patterns

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
