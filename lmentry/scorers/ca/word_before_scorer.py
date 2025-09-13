import re

from lmentry.scorers.ca.scorer import LMentryScorer, the_sentence_regex, the_word_regex, swap_substrings


class WordBeforeScorer(LMentryScorer):
    """This class was created by simply mirroring `WordAfterScorer`
    """
    def __init__(self):
        super().__init__()

        self.prefixes.extend([
            "A la frase {sentence} ",
            "A {sentence} ",
        ])

        self.suffixes.extend([
            " a la frase {sentence}",
            " a {sentence}",
        ])

    def get_base_patterns(self, answer, query, sentence):

        before = r"(immediatament |just )?abans de"
        comes = r"(va|ve)"

        base_patterns = [
            rf"{answer} {comes} {before} {query}",
            rf"{answer} és la paraula que {comes} {before} {query}",
            rf"{answer} és la paraula {before} {query}",
            rf"La paraula que {comes} {before} {query} és {answer}",
            rf"La paraula que {comes} {before} {query} a {sentence} és {answer}",
            rf"La paraula {before} {query} és {answer}",
            rf"{query} precedeix a {answer}",
        ]

        # replace before with after and swap answer and query
        after = r"(immediatament |just )?després de"
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

        answer = the_word_regex(answer)
        query = the_word_regex(query)
        sentence = the_sentence_regex(sentence)

        score, certainty = self._simple_scorer(prediction, answer)
        if score:
            return score, certainty

        base_patterns = self.get_base_patterns(answer, query, sentence)
        self.prefix_kwargs = {"sentence": sentence}
        self.suffix_kwargs = {"sentence": sentence}

        score, certainty = self.certainty_scorer(prediction, base_patterns)
        return score, certainty
