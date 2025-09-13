import re

from lmentry.eu_declension import possessive_genitive_undetermined
from lmentry.scorers.eu.scorer import LMentryScorer, the_word_regex, swap_substrings


class WordBeforeScorer(LMentryScorer):
    """This class was created by simply mirroring `WordAfterScorer`
    """
    def __init__(self):
        super().__init__()

        # 'Q: "{sentence}" esaldian, zein hitz dago "{word}" aurre-aurretik?\nA:'
        # 'Q: "{sentence}" esaldian, zein hitz dago "{word}" aurretik?\nA:'
        # 'Q: Zein hitz dator "{word}" baino lehen "{sentence}" esaldian?\nA:'

        self.prefixes.extend([
            r"\"?{sentence}\"? esaldian,? ",
            r"Esaldi (honetan|horretan),? ",
        ])

        self.suffixes.extend([
            r" \"?{sentence}\"? esaldian",
            r" esaldi (honetan|horretan)",
        ])

    def get_base_patterns(self, answer, query, sentence):

        answer = rf"\"?{answer}\"?( hitza)?"
        query = rf"\"?{query}\"?"
        before = r"(aurre-aurretik|aurretik|baino lehen)"
        comes = r"(dator|doa|dago)"
        of_query = rf"({query}( hitza)?|{query}( hitzaren)?|{possessive_genitive_undetermined(query[3:-3])})"

        base_patterns = [
            rf"{of_query} {before} {answer} {comes}",
            rf"{answer} {comes} {of_query} {before}",
            rf"{of_query} {before} (datorren|doan|dagoen) hitza {answer} da",
            rf"{answer} da {of_query} {before} (datorren|doan|dagoen) hitza",
            rf"{of_query} ondorengo hitza {answer} da",
            rf"{answer} da {of_query} ondorengo hitza",
        ]

        # replace before with after and swap answer and query
        after = r"(atze-atzetik|atzetik|ondoren|eta gero)"
        more_base_patterns1 = [
            swap_substrings(s, subs1=answer, subs2=query).replace(before, after)
            for s in base_patterns
            if before in s
        ]
        base_patterns.extend(more_base_patterns1)

        return base_patterns + self.get_shared_patterns(target=answer)

    def negative_scorer(self, prediction, answer, sentence):
        score, certainty = None, None

        if not re.search(rf"\b{answer}\b", prediction):
            score = 0
            certainty = 1

        if re.sub(r'[^\w ]+', '', prediction) == sentence:
            score = 0
            certainty = 1

        return score, certainty

    def score_prediction(self, prediction, example, truncate_prediction: bool = False):
        prediction = self.normalize_prediction(prediction, truncate_prediction)

        metadata = example["metadata"]
        answer = metadata["answer"]
        query = metadata["query"]
        sentence = metadata["sentence"]

        # in the word before/after tasks, the sentence, the answer, and the query are saved in their
        # original case as many sentence words are named entities. in scoring, we choose to ignore
        # the case.
        answer = answer.lower()
        query = query.lower()
        sentence = sentence.lower()

        score, certainty = self.negative_scorer(prediction, answer, sentence)
        if score is not None:
            return score, certainty

        score, certainty = self._simple_scorer(prediction, the_word_regex(answer))
        if score:
            return score, certainty

        base_patterns = self.get_base_patterns(answer, query, sentence)
        self.prefix_kwargs = {"sentence": sentence}
        self.suffix_kwargs = {"sentence": sentence}

        score, certainty = self.certainty_scorer(prediction, base_patterns)
        return score, certainty
