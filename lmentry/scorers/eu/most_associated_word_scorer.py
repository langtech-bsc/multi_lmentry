import re

from lmentry.eu_abstract_categories import eu_abstract_categories
from lmentry.eu_declension import comitative_singular, comitative_plural, absolutive_singular, absolutive_plural
from lmentry.scorers.eu.scorer import LMentryScorer, the_word_regex, the_words_regex


class MostAssociatedWordScorer(LMentryScorer):
    def __init__(self):
        super().__init__()

        # Q: {options} hitzen artean, zeinek du lotura gehien "{category}" kategoriarekin?
        # Q: Zein hitz erlazionatzen da gehien "{category}" kategoriarekin {options} hitzen artean?
        # Hurrengo hitzen artean, aukeratu "{category}" kategoriarekin lotura gehien duen hitza - {options}

        # we use `[^a-zA-Z0-9_]` instead of `\W` as we always lowercase the pattern in
        # `certainty_scorer`. See the to-do suggestion in normalize_string

        self.prefixes.extend([
            r"{words} hitzen artean,? ",
            r"{words} hitzetatik,? ",
            r"Hitz (hauen|horien) artean,? ",
            r"Hitz (hauetatik|horietatik),? "
        ])

        self.suffixes.extend([
            r" {words} hitzen artean",
            r" hitz (hauen|horien) artean"
        ])

    def get_base_patterns(self, answer, category, words):

        declensed_category = absolutive_singular(category) if category in eu_abstract_categories else absolutive_plural(category)
        derivation_func = comitative_singular if category in eu_abstract_categories else comitative_plural

        answer = rf"\"?{answer}\"?"
        declensed_category = rf"\"?{declensed_category}\"?"
        with_category = f"(kategoriarekin|kategoria honekin|kategoria horrekin|{derivation_func(category)}|{declensed_category} {comitative_singular('kategoria')})"
        has = r"(du|dauka)"
        more = r"(gehien|gehiago)"
        relation = r"(lotura|erlazio|zerikusi)"

        base_patterns = [
            rf"{answer}( hitza)? da",
            rf"{answer}( hitza)? da {with_category} {relation} {more} (duena|daukana)",
            rf"{with_category} {relation} {more} (duena|daukana) {answer}( hitza)? da",
            rf"{answer}( hitza)? da {with_category} {relation} {more} (duen|daukan) hitza",
            rf"{with_category} {relation} {more} (duen|daukan) hitza {answer}( hitza)? da",
            rf"{answer}( hitza)? {more} erlazionatzen da",
            rf"{answer}( hitza)? erlazionatzen da {more}",
            rf"{answer}( hitza)? da {with_category} {more} erlazionatzen (dena|den hitza)",
            rf"{with_category} {more} erlazionatzen (dena|den hitza) {answer}( hitza)? da",
            rf"{answer} hitzak {has} {relation} {more}",
            rf"{answer} hitzak {has} {relation} {more} {with_category}",
            rf"{with_category} {answer} hitzak {has} {relation} {more}"
        ]

        return base_patterns + self.get_shared_patterns(target=answer)

    def get_exact_patterns(self, answer, category):
        return [
            rf"{answer}",
            rf"{category} - {answer}"
        ]

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

        category = metadata["category"]
        distractors = metadata["distractors"]
        answer_index = metadata["answer_index"]
        words = distractors[:answer_index] + [answer] + distractors[answer_index:]

        exact_patterns = self.get_exact_patterns(the_word_regex(answer), the_word_regex(category))
        for exact_pattern in exact_patterns:
            score, certainty = self._simple_scorer(prediction, answer=exact_pattern)
            if score:
                return score, certainty

        words = the_words_regex(words)

        base_patterns = self.get_base_patterns(answer, category, words)

        self.prefix_kwargs = {"words": words}
        self.suffix_kwargs = {"words": words}

        score, certainty = self.certainty_scorer(prediction, base_patterns)
        return score, certainty
