from lmentry.scorers.eu.scorer import LMentryScorer, the_word_regex, the_letter_regex


class WordContainingScorer(LMentryScorer):
    def __init__(self):
        super().__init__()

        # 'Idatzi "{letter}" letra duen hitz bat:\n'
        # 'Idatzi hitz bat "{letter}" letra daukana:\n'
        # 'Idatzi hitz bat zeinetan "{letter}" letra agertzen den:\n'

    def get_base_patterns(self, letter, word):

        that_has = r"(daukan|duen)"
        letter = rf"\"?{letter}\"?"

        base_patterns = [
            rf"{letter}( letra)? {that_has} hitz bat {word} da",
            rf"{letter}( letra)? {that_has} hitz bat da {word}",
            rf"{word} {letter}( letra)? {that_has} hitz bat da",
            rf"{letter}( letra)? {that_has} hitz bat: {word}",
            rf"hitz bat zeinetan {letter} agertzen den: {word}",
            rf"{word} hitzean {letter} letra agertzen da",
            rf"{letter} letra agertzen da {word} hitzean",
            rf"{word} hitzak {letter} letra (du|dauka)",
            rf"{letter} letra (du|dauka) {word} hitzak",
        ]

        return base_patterns + self.get_shared_patterns(target=word)

    def score_prediction(self, prediction, example, truncate_prediction: bool = False):
        prediction = self.normalize_prediction(prediction, truncate_prediction)

        letter = example["metadata"]["letter"]

        # the third option under `else` is for cases like "e-mail" and "x-ray"
        word = rf"((\w+{letter}\w*)|(\w*{letter}\w+)|({letter}-\w+))"

        score, certainty = self._simple_scorer(prediction, the_word_regex(word))
        if score:
            return score, certainty

        letter = the_letter_regex(letter)
        base_patterns = self.get_base_patterns(letter, word)

        score, certainty = self.certainty_scorer(prediction, base_patterns)
        return score, certainty
