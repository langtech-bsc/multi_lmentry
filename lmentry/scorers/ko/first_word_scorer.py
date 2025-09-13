import re

from lmentry.scorers.ko.scorer import LMentryScorer, the_sentence_regex, the_word_regex


class FirstWordScorer(LMentryScorer):
    def __init__(self):
        super().__init__()

        self.prefixes.extend([
            "다음 {sentence}에서 ",
        ])

        self.suffixes.extend([
            " (의|에서) {sentence}",
        ])

    def get_base_patterns(self, answer, sentence):
        is_ = r"(이|가|은|는|와|과|의|에서|을|를)"
        base_patterns = [
            rf"첫 번째 단어는 {answer}입니다",
            rf"{sentence}{is_} 첫 번째 단어는 {answer}입니다",
            rf"{answer}{is_} 첫 번째 단어입니다",
            rf"{sentence}{is_} {answer}로 시작합니다",
            rf"첫 단어\W+{answer}",
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

        answer = the_word_regex(answer)
        sentence = the_sentence_regex(sentence)

        score, certainty = self._simple_scorer(prediction, answer)
        if score:
            return score, certainty

        base_patterns = self.get_base_patterns(answer, sentence)
        self.prefix_kwargs = {"sentence": sentence}
        self.suffix_kwargs = {"sentence": sentence}

        score, certainty = self.certainty_scorer(prediction, base_patterns)
        return score, certainty
