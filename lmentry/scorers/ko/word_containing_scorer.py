from lmentry.scorers.ko.scorer import LMentryScorer, the_word_regex, the_letter_regex


class WordContainingScorer(LMentryScorer):
    def __init__(self):
        super().__init__()

    def get_base_patterns(self, letter, word):
        is_ = r"(이|가|은|는|와|과|의|에서|을|를)"
        contains = r"(포함하는|사용하는|가지고 있는)"
        
        base_patterns = [
            rf"{word}{is_} {letter}{is_} {contains} 단어입니다",
            rf"{word}{is_} {letter}{is_} (포함 합니다|포함하고 있습니다)",
        ]


        return base_patterns + self.get_shared_patterns(target=word)

    def score_prediction(self, prediction, example, truncate_prediction: bool = False):
        prediction = self.normalize_prediction(prediction, truncate_prediction)

        letter = example["metadata"]["letter"]

        word = (rf"\w*{letter}\w*"
                if letter in {"a", "i"}
                else rf"((\w+{letter}\w*)|(\w*{letter}\w+)|({letter}-\w+))"
                # the third option under `else` is for cases like "e-mail" and "x-ray"
                )
        word = the_word_regex(word)

        score, certainty = self._simple_scorer(prediction, word)
        if score:
            return score, certainty

        letter = the_letter_regex(letter)
        base_patterns = self.get_base_patterns(letter, word)

        score, certainty = self.certainty_scorer(prediction, base_patterns)
        return score, certainty
