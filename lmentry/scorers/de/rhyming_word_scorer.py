import re

from lmentry.scorers.en.scorer import LMentryScorer, the_word_regex, swap_substrings


class RhymingWordScorer(LMentryScorer):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_exact_patterns(answer, query, distractor):

        a = r"(ein|das)"
        while_ = "(während)"
        exact_patterns = [
            rf"{query} reimt sich auf {answer}( und nicht auf {distractor})?",
            rf"{query} ist {a} Reimwort von {answer}( und nicht von {distractor})?",
            rf"{query} und {answer} reimen sich",
            rf"{query} und {answer} sind Reimwörter",
            rf"{query} und {answer} sind Wörter, die sich reimen",
            rf"{a} Reimwort von {query} ist {answer}( und nicht {distractor})?",
            rf"{a} Wort, das sich auf {query} reimt, ist {answer}",
            rf"{query} und {answer} reimen sich( aufeinander)?, {while_} {distractor} sich auf keines von beiden reimt"
        ]

        # swap answer and query
        more_exact_patterns = [
            swap_substrings(s, subs1=answer, subs2=query) for s in exact_patterns
        ]
        exact_patterns.extend(more_exact_patterns)

        more_exact_patterns_2 = [
            rf"{distractor} reimt sich nicht auf {query}(\s+{answer} reimt sich auf {query})?",
            rf"{query} reimt sich nicht auf {distractor}(\s+{query} reimt sich auf {answer})?",
            rf"{answer} reimt sich auf {query}\s+{distractor} reimt sich nicht auf {query}",
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
