import re

from lmentry.eu_declension import comitative_singular, instrumental_singular
from lmentry.scorers.eu.scorer import LMentryScorer


class EndsWithWordScorer(LMentryScorer):
    def __init__(self):
        super().__init__()

        # 'Idatzi "{word}" hitzarekin amaitzen den esaldi bat:\n'
        # 'Idatzi esaldi bat zeinen azken hitza "{word}" den:\n'
        # 'Idatzi esaldi bat "{word}" hitzarekin amaituz:\n'

        last = "(azken|azkenengo|amaierako|bukaerako)"
        word = r"\"?{word}\"?"
        with_word = fr"({word} {instrumental_singular('hitz')}|{word} {comitative_singular('hitz')})"
        a_sentence = r"(esaldia|esaldi bat)"
        finishing = r"(amaitzen|bukatzen)"

        self.prefixes.extend([
            rf"{with_word} {finishing} den {a_sentence}( da)? ",
            rf"{with_word} {finishing} den {a_sentence}: ",
        ])

        self.suffixes.extend([
            r" da",
            fr" esaldian, {last} hitza {word} da",
            fr" esaldiaren {last} hitza {word} da",
        ])

    def get_base_patterns(self, word):

        # we want a word to contain at least two letters
        valid_word = r"(\w\w+)"
        # we use `[^a-zA-Z0-9_]` instead of `\W` as we always lowercase the pattern in
        # `_certainty_scorer`.
        # we can't tell if the sentence words are actual English words, but as a sanity we demand at
        # least one additional "word" before the ending word
        allowed_sentence = rf".*{valid_word}[^a-zA-Z0-9_]+{word}[^a-zA-Z0-9_]*"

        base_patterns = [
            allowed_sentence
        ]
        return base_patterns + self.get_shared_patterns(target=allowed_sentence)
    
    def negative_scorer(self, prediction, word):
        score, certainty = None, None

        if not re.search(rf"\b{word}\b", prediction):
            score = 0
            certainty = 1

        return score, certainty

    def score_prediction(self, prediction, example, truncate_prediction: bool = False):
        prediction = self.normalize_prediction(prediction, truncate_prediction)

        word = example["metadata"]["word"].lower()
        score, certainty = self.negative_scorer(prediction, word)
        if score is not None:
            return score, certainty

        base_patterns = self.get_base_patterns(word)

        # note that the second case of `_simple_scorer` is not relevant
        score, certainty = self._simple_scorer(prediction, base_patterns[0])
        if score:
            return score, certainty

        self.prefix_kwargs = {"word": word}
        self.suffix_kwargs = {"word": word}

        score, certainty = self.certainty_scorer(prediction, base_patterns)
        return score, certainty
