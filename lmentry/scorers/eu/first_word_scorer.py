import re

from lmentry.eu_declension import *
from lmentry.scorers.eu.scorer import LMentryScorer, the_word_regex


class FirstWordScorer(LMentryScorer):
    def __init__(self):
        super().__init__()

        # 'Q: Zein da "{sentence}" esaldiaren lehenengo hitza?\nA:'
        # 'Q: "{sentence}" esaldian, zein da lehenengo hitza?\nA:'
        # 'Idatzi "{sentence}" esaldiaren lehenengo hitza:\n'

    def get_base_patterns(self, answer, sentence):

        answer = rf"\"?{answer}\"?"
        sentence = rf"\"?{sentence}\"?"

        first = r"(lehen|lehenengo|hasierako)"
        opening = "hasiera"
        start = "hasten"
        the_sentence = fr"({sentence} esaldia|esaldia|esaldi hori|esaldi hau)"
        of_sentence = f"(({sentence} )?({possessive_genitive_singular('esaldi')}|{local_genitive_singular('esaldi')}))"
        with_word = f"({comitative_singular('hitz')}|{instrumental_singular('hitz')})"

        base_patterns = [
            rf"{answer} da",
            rf"{answer} hitza da",
            rf"{first} hitza {answer}( hitza)? da",
            rf"{answer}( hitza)? da {first} hitza",
            rf"{first} hitza: {answer}",
            rf"{of_sentence} {first} hitza {answer}( hitza)? da",
            rf"{answer}( hitza)? da {of_sentence} {first} hitza",
            rf"{of_sentence} {opening} {answer} da",
            rf"{answer} da {of_sentence} {opening}",
            rf"{of_sentence} {first} hitza: {answer}",
            fr"{the_sentence} {answer} {with_word} {start} da"
            fr"{answer} {with_word} {start} da {the_sentence}"
        ]

        return base_patterns + self.get_shared_patterns(target=answer)

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
        sentence = metadata["sentence"]

        # in the first/last word tasks, the sentence and the answer are saved in their original case
        # as many sentence words are named entities. in scoring, we choose to ignore the case.
        answer = answer.lower()
        sentence = sentence.lower()
        
        score, certainty = self.negative_scorer(prediction, answer)
        if score is not None:
            return score, certainty

        score, certainty = self._simple_scorer(prediction, the_word_regex(answer))
        if score:
            return score, certainty

        base_patterns = self.get_base_patterns(answer, sentence)
        self.prefix_kwargs = {"sentence": sentence}
        self.suffix_kwargs = {"sentence": sentence}

        score, certainty = self.certainty_scorer(prediction, base_patterns)
        return score, certainty
