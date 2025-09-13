import re

from lmentry.scorers.pt_br.scorer import LMentryScorer, the_word_regex, swap_substrings


class RhymingWordScorer(LMentryScorer):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_exact_patterns(answer, query, distractor):

        a = r"(uma|a)"
        while_ = "(enquanto|mas|e)"
        exact_patterns = [
            rf"{query} rima com {answer}( e não com {distractor})?",
            rf"{query} é {a} rima de {answer}( e não de {distractor})?",
            rf"{query} e {answer} rimam",
            rf"{query} e {answer} são palavras que rimam",
            rf"{a} rima de {query} é {answer}( e não {distractor})?",
            rf"{a} palavra que rima com {query} é {answer}",
            rf"{query} é {answer} rimam, {while_} {distractor} não rima( com nenhuma)?"
        ]

        # swap answer and query
        more_exact_patterns = [
            swap_substrings(s, subs1=answer, subs2=query) for s in exact_patterns
        ]
        exact_patterns.extend(more_exact_patterns)

        more_exact_patterns_2 = [
            rf"{distractor} não rima com {query}(\s+{answer} rima com {query})?",
            rf"{query} não rima com {distractor}(\s+{query} rima com {answer})?",
            rf"{answer} rima com {query}\s+{distractor} no rima com {query}",
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
