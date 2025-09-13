import re

from lmentry.scorers.en.scorer import LMentryScorer


class AllWordsFromCategoryScorer(LMentryScorer):
    def __init__(self):
        super().__init__()

    def get_base_patterns(self, answer, category):

        all_words = r"(all die Wörter|alle der Wörter|alle Wörter|alle)"
        listed = r"(,die aufgelistet sind,|in der Liste)"
        belong = r"(repräsentieren|sind Arten von|sind Beispiele von|gelten als Arten von)"

        base_patterns = [
            rf"{answer}, die Liste enthält nur {category}",
            rf"{answer}, {all_words}( {listed})? {belong} {category}",
            rf"^{answer}\b",
        ]

        return base_patterns + self.get_shared_patterns(target=answer)

    @staticmethod
    def category_regex(category):
        if category == "items of clothing":
            category = rf"({category}|clothes|clothing)"
        elif category == "furniture":
            category = rf"({category}|pieces of furniture)"
        elif category == "fruit":
            category = rf"({category}|fruits)"

        return category

    @staticmethod
    def negative_scorer(prediction, answer):
        score = None
        certainty = None

        opposite_answer = "no" if answer == "yes" else "yes"
        if re.match(rf"{opposite_answer}\.?$", prediction):
            score = 0
            certainty = 1

        return score, certainty

    def score_prediction(self, prediction, example, truncate_prediction: bool = False):
        prediction = self.normalize_prediction(prediction, truncate_prediction)

        metadata = example["metadata"]
        answer = "yes" if metadata["num_distractors"] == 0 else "no"

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
