import re

from lmentry.eu_declension import ergative_undetermined, comitative_singular
from lmentry.scorers.eu.scorer import LMentryScorer, the_word_regex, swap_substrings


class RhymingWordScorer(LMentryScorer):
    def __init__(self):
        super().__init__()

    # "Q: Hauetako zeinek errimatzen du \"{query}\" hitzarekin: \"{word1}\" edo \"{word2}\"?\nA:"
    # "Q: Hauetako zeinek du errima \"{query}\" hitzarekin: \"{word1}\" edo \"{word2}\"?\nA:"
    # "Q:  \"{word1}\" eta \"{word2}\" hitzen artean, zeinek errimatzen du \"{query}\" hitzarekin?\nA:"

    @staticmethod
    def get_exact_patterns(answer, query, distractor):

        the_answer = rf"(\"?{answer}\"?( hitzak?)?|{ergative_undetermined(answer)})"
        the_query = rf"(\"?{query}\"?( hitzak?)?|{ergative_undetermined(query)})"
        with_query = rf"(\"?{query}\"?( hitzarekin?)?|{comitative_singular(query)})"

        with_answer = rf"(\"?{answer}\"?( hitzarekin?)?|{comitative_singular(answer)})"

        has = r"(du|dauka)"
        together = r"( elkarrekin|elkarren artean)?"

        exact_patterns = [
            rf"{the_answer}",
            rf"{the_answer} {with_query} errimatzen du",
            rf"{the_query} {with_answer} errimatzen du",
            rf"{the_answer} errimatzen du {with_query}",
            rf"{the_query} errimatzen du {with_answer}",
            rf"{the_answer} {with_query} errima {has}",
            rf"{the_query} {with_answer} errima {has}",
            rf"{the_answer} errima {has} {with_query}",
            rf"{the_query} errima {has} {with_answer}",
            rf"{the_answer} eta {the_query}{together} errima (dute|daukate)",
            rf"{the_query} eta {the_answer}{together} errima (dute|daukate)",
            rf"{the_answer} eta {the_query}{together} errimatzen dute",
            rf"{the_query} eta {the_answer}{together} errimatzen dute",
            rf"{the_answer} eta {the_query}{together} errimatzen duten hitzak dira",
            rf"{the_query} eta {the_answer}{together} errimatzen duten hitzak dira",
            rf"{the_answer} eta {the_query}( hitzak)? dira{together} errimatzen dutenak",
            rf"{the_query} eta {the_answer}( hitzak)? dira{together} errimatzen dutenak",
            rf"{the_answer} eta {the_query}{together} errima (dute|daukate)",
            rf"{the_query} eta {the_answer}{together} errima (dute|daukate)",
            rf"{the_answer} eta {the_query}( hitzak)? dira{together} errima (dutenak|daukatenak)",
            rf"{the_query} eta {the_answer}( hitzak)? dira{together} errima (dutenak|daukatenak)",
            rf"{with_query} errimatzen (duena|duen hitza) {the_answer} da",
            rf"{with_answer} errimatzen (duena|duen hitza) {the_query} da",
            rf"{with_query} errima (duena|daukana|duen hitza|daukan hitza) {the_answer} da",
            rf"{with_answer} errima (duena|daukana|duen hitza|daukan hitza) {the_query} da"
        ]

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

        score, certainty = self._simple_scorer(prediction, the_word_regex(answer))
        if score:
            return score, certainty

        query = metadata["query"]
        distractor = metadata["distractor"]

        exact_patterns = self.get_exact_patterns(answer, query, distractor)

        for exact_pattern in exact_patterns:
            score, certainty = self._simple_scorer(prediction, exact_pattern)
            if score:
                return score, certainty
        else:
            score = 0
            certainty = 0

        return score, certainty
