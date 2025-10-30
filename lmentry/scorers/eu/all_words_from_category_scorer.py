import re

from lmentry.eu_declension import absolutive_plural, comitative_singular
from lmentry.scorers.eu.scorer import LMentryScorer
from lmentry.eu_abstract_categories import eu_abstract_categories


class AllWordsFromCategoryScorer(LMentryScorer):
    def __init__(self):
        super().__init__()

    # 'Q: {words} hitzetako guztiak {category:ak} dira? Erantzun "bai" edo "ez".\nA:'
    # 'Q: {words} hitzetako guztiek {category:ak} adierazten dituzte ? Erantzun "bai" edo "ez".\nA:'
    # 'Q: [{words}] zerrendak {category:ak} besterik ez ditu? Erantzun "bai" edo "ez".\nA:'

    def get_base_patterns(self, answer, category):

        all_words = r"(hitzetako guzti[ae]k|hitz (horietako|horiek)? guzti[ae]k|hitz guzti horiek|hitzak|guztiak)"
        listed = r"(zerrendako|zerrendatutako|aipatutako|emandako)"
        belong = r"(dira|adierazten dituzte)"

        base_patterns = [
            rf"{answer}, zerrendak {category} besterik ez (ditu|dauzka)",
            rf"{answer}, zerrendak {category} besterik ez ditu aipatzen",
            rf"{answer}, zerrendan {category} besterik ez daude",
            rf"{answer}, {category} besterik ez dira( aipatzen)?",
            rf"{answer}, guztiak dira {category}",
            rf"{answer}, ({listed} )?({all_words} )?{category} {belong}",
            rf"^{answer}\b",
        ]

        return base_patterns + self.get_shared_patterns(target=answer)

    @staticmethod
    def category_regex(category):
        category = category.replace(" eta ", " edo ")
        if category in eu_abstract_categories:
            category = f"{comitative_singular(category)} ((lotura|zerikusia|erlazioa) duten|(lotuta|erlazionatuta) dauden) hitz"
        category = absolutive_plural(category)
        return category

    @staticmethod
    def negative_scorer(prediction, answer):
        score = None
        certainty = None

        opposite_answer = "ez" if answer == "bai" else "bai"
        if re.match(rf"{opposite_answer}\.?$", prediction):
            score = 0
            certainty = 1

        return score, certainty

    def score_prediction(self, prediction, example, truncate_prediction: bool = False):
        prediction = self.normalize_prediction(prediction, truncate_prediction)

        metadata = example["metadata"]
        answer = "bai" if metadata["num_distractors"] == 0 else "ez"

        score, certainty = self.negative_scorer(prediction, answer)
        if score is not None:
            return score, certainty

        score, certainty = self._simple_scorer(prediction, answer)
        if score:
            return score, certainty

        category = metadata["category"]
        category = AllWordsFromCategoryScorer.category_regex(category)

        base_patterns = self.get_base_patterns(answer, category)
        score, certainty = self.certainty_scorer(prediction, base_patterns)

        return score, certainty
