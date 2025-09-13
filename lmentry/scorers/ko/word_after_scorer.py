import re

from lmentry.scorers.ko.scorer import LMentryScorer, the_sentence_regex, the_word_regex, swap_substrings


class WordAfterScorer(LMentryScorer):
    def __init__(self):
        super().__init__()

        self.prefixes.extend([
            "다음 문자에서: {sentence} ",
        ])

        self.suffixes.extend([
            "문장 {sentence} 안에",
        ])

    def get_base_patterns(self, answer, query, sentence):

        after = r"(다음에|후에|뒤에)"
        succeeds = r"(따르는|뒤를 잇는)"
        is_ = r"(이|가|은|는|와|과|의|에서)"
        
        base_patterns = [
            rf"{answer}{is_} {query}의 {after} 옵니다",
            rf"{answer}{is_} {query}의 {after} 오는 단어입니다",
            rf"{query}의 {after} 오는 단어는 {answer}입니다",
            rf"{query}{is_} {succeeds} 단어는 {answer}입니다"
        ]

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

        # in the word after/before tasks, the sentence, the answer, and the query are saved in their
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
