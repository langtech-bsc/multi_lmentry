import re

from lmentry.scorers.ca.scorer import LMentryScorer


class AllWordsFromCategoryScorer(LMentryScorer):
    def __init__(self):
        super().__init__()

    def get_base_patterns(self, answer, category):

        all_words = r"(totes aquestes paraules|totes les paraules|totes elles|entre aquestes paraules, totes|totes)"
        listed = r"(llistades|de la llista)"
        belong = r"(representen|són tipus de|fan referència a|es refereixen a|són exemples de|contenen exclusivament)"

        base_patterns = [
            rf"{answer}, la llista inclou exclusivament {category}",
            rf"{answer}, la llista només inclou {category}",
            rf"{answer}, les paraules {listed} {belong} {category}"
            rf"{answer}, {all_words}( {listed})? {belong} {category}",
            rf"^{answer}\b",
        ]

        return base_patterns + self.get_shared_patterns(target=answer)

    @staticmethod
    def category_regex(category):
        if category == "membres de la família":
            category = rf"({category}|relacions familiars)"
        elif category == "conceptes geogràfics":
            category = rf"({category}|conceptes de geografia)"
        elif category == "components de la llar":
            category = rf"({category}|conceptes de la llar)"
        elif category == "instruments":
            category = rf"({category}|instruments musicals)"
        elif category == "peces de roba":
            category = rf"({category}|roba)"
        elif category == "conceptes del cicle vital":
            category = rf"({category}|conceptes de la vida)"
        
        return category

    @staticmethod
    def negative_scorer(prediction, answer):
        score = None
        certainty = None

        opposite_answer = "no" if answer == "sí" else "sí"
        if re.match(rf"{opposite_answer}\.?$", prediction):
            score = 0
            certainty = 1

        return score, certainty

    def score_prediction(self, prediction, example, truncate_prediction: bool = False):
        prediction = self.normalize_prediction(prediction, truncate_prediction)

        metadata = example["metadata"]
        answer = "sí" if metadata["num_distractors"] == 0 else "no"

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
