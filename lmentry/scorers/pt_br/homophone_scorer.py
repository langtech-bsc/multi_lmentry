import re

from lmentry.scorers.pt_br.scorer import LMentryScorer, the_word_regex, swap_substrings


class HomophoneScorer(LMentryScorer):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_exact_patterns(answer, query, distractor):

        _but = r"(\.,)? (mas|e)"
        like = "(como|similar a|parecido com|igual a)"

        exact_patterns = [
            rf"{query} soa {like} {answer}",
            rf"{query} soa {like} {answer}{_but} não {like} {distractor}",
            rf"{query} soa {like} {answer}{_but} {distractor} não",
            rf"{query} e {answer} soam (igual|similar)",
            rf"{query} y {answer} se pronunciam (igual|de maneira similar)",
            rf"{query} soa mais {like} {answer}",
            rf"{query} soa mais {like} {answer} que {distractor}",
            rf"{query} soa mais {like} {answer}",
            rf"{query} é  (homófono|homófona) de {answer}",
            rf"{query} é um homófono de {answer}",
            rf"{query} é uma palavra homófona {answer}",
            rf"{query} y {answer} são homófonas",
            rf"{query} y {answer} são palavras homófonas",
            rf"O homófono de {query} é {answer}",
            rf"A palavra homófona de {query} é {answer}",
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
