import re

from lmentry.scorers.ko.scorer import (
    LMentryScorer, swap_substrings, the_word_regex, standardized_number_regex
)


class LessLettersScorer(LMentryScorer):
    """This class was created by simply mirroring `MoreLettersScorer`
    """
    def __init__(self):
        super().__init__()

        self.prefixes.extend([
            "{word1}과 {word2} 중에서, ",
        ])

    def get_base_patterns(self, answer, distractor, diff):

        is_ = r"(이|가|은|는|와|과|의|에서|을|를)"
        less = r"(적습니다|더 적다|더 적습니다|적다)"
        base_patterns = [
            rf"{answer}{is_} 글자 수가 {less}",
            rf"{answer}{is_} {distractor}보다 글자 수가 {less}",
            rf"{answer}{is_} {diff}개의 글자가 {less}",
            rf"{answer}{is_} {distractor}보다 {diff}개의 글자가 {less}",
            rf"글자 수가 (적은|더 적은) 단어는 {answer}입니다",
            rf"{answer}{is_} 글자 수가 (적은|더 적은) 단어입니다",
            rf"{answer}{is_} 더 짧습니다",
            rf"{answer}{is_} {distractor}보다 짧습니다",
            rf"{answer}{is_} {distractor}보다 {diff}글자만큼 짧습니다",
            rf"더 짧은 단어는 {answer}입니다",
            rf"더 짧은 단어는 {answer}입니다",
            rf"{answer}는 더 짧은 단어입니다",
        ]

        more_base_patterns1 = [
            swap_substrings(s, subs1=answer, subs2=distractor).replace(less, "more")
            for s in base_patterns
            if less in s
        ]
        base_patterns.extend(more_base_patterns1)

        # replace shorter with longer and swap answer and distractor
        more_base_patterns2 = [
            swap_substrings(s, subs1=answer, subs2=distractor).replace("shorter", "longer")
            for s in base_patterns
            if "shorter" in s
        ]
        base_patterns.extend(more_base_patterns2)

        return base_patterns + self.get_shared_patterns(target=answer)
    
    def negative_scorer(self, prediction, answer, distractor, diff):
        score, certainty = None, None

        less = r"(적습니다|더 적다|더 적습니다|적다)"
        is_ = r"(이|가|은|는|와|과|의|에서)"
        
        negative_patterns = [
            distractor,
            rf"{distractor}{is_} 글자 수가 {less}",
            rf"{distractor}{is_} {answer}보다 글자 수가 {less}",
            rf"{distractor}{is_} {diff}개의 글자가 {less}",
            rf"{distractor}{is_} {answer}보다 {diff}개의 글자가 {less}",
            rf"글자 수가 {less}인 단어는 {distractor}입니다",
            rf"{distractor}{is_} 글자 수가 (적은|더 적은) 단어입니다",
            rf"{distractor}{is_} 더 짧습니다",
            rf"{distractor}{is_} {diff}글자만큼 더 짧습니다",
            rf"{distractor}{is_} {answer}보다 짧습니다",
            rf"{distractor}{is_} {answer}보다 {diff}글자만큼 짧습니다",
            rf"더 짧은 단어는 {distractor}입니다",
            rf"더 짧은 단어는 {distractor}입니다",
            rf"{distractor}{is_} 더 짧은 단어입니다",
        ]

        
        for negative_pattern in negative_patterns:
            negative_pattern = self.normalize_string(negative_pattern)
            if re.match(rf"{negative_pattern}\.?$", prediction):
                score = 0
                certainty = 1
                break
                
        is_ = r"(이|가|은|는|와|과|의|에서)"
        number_regex = r"(?P<number>\d+|한|두|세|네|다섯|여섯|일곱|여덟|아홉|열|영|하나)"
        wrong_diff_patterns = [
            rf"{answer}{is_} 글자 수가 {number_regex} 개 {less}",
            rf"{answer}{is_} {distractor}보다 글자 수가 {number_regex} 개 {less}",
            rf"{answer}{is_} {number_regex} 글자만큼 {less}",
            rf"{answer}{is_} {distractor}보다 {number_regex} 글자만큼 {less}",
        ]

        for wrong_diff_pattern in wrong_diff_patterns:
            if res := re.match(wrong_diff_pattern, prediction):
                predicted_diff = res.group("number")
                if not re.match(diff, predicted_diff):
                    score = 0
                    certainty = 1
                    break

        return score, certainty

    def score_prediction(self, prediction, example, truncate_prediction: bool = False):
        prediction = self.normalize_prediction(prediction, truncate_prediction)

        metadata = example["metadata"]
        answer = metadata["answer"]

        distractor = metadata["distractor"]
        diff = len(distractor) - len(answer)
        word1 = metadata["word1"]
        word2 = metadata["word2"]

        answer = the_word_regex(answer)
        distractor = the_word_regex(distractor)
        diff = standardized_number_regex(diff)
        word1 = the_word_regex(word1)
        word2 = the_word_regex(word2)
        
        score, certainty = self.negative_scorer(prediction, answer, distractor, diff)
        if score is not None:
            return score, certainty

        score, certainty = self._simple_scorer(prediction, answer)
        if score:
            return score, certainty

        base_patterns = self.get_base_patterns(answer, distractor, diff)
        self.prefix_kwargs = {"word1": word1, "word2": word2}

        score, certainty = self.certainty_scorer(prediction, base_patterns)
        return score, certainty
