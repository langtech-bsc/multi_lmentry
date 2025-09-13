import re

from lmentry.scorers.es.scorer import (
    LMentryScorer, swap_substrings, the_word_regex, standardized_number_regex
)


class MoreLettersScorer(LMentryScorer):

    def __init__(self):
        super().__init__()

        self.prefixes.extend([
            "De las palabras {word1} y {word2}, ",
            "Entre las palabras {word1} y {word2}, ",
        ])

    def get_base_patterns(self, answer, distractor, diff):

        base_patterns = [
            rf"{answer} tiene más letras",
            rf"{answer} tiene más letras que {distractor}",
            rf"{answer} tiene {diff} letra(s)? más",
            rf"{answer} tiene {diff} letra(s)? más que {distractor}",
            rf"La palabra que tiene más letras es {answer}",
            rf"{answer} es la palabra con más letras",
            rf"{answer} es más larga",
            rf"{answer} es más larga que {distractor}",
            rf"{answer} es más larga que {distractor} por {diff} letra(s)?",
            rf"La palabra más larga es {answer}",
            rf"{answer} es la palabra más larga",
        ]
        # replace more with less or fewer and swap answer and distractor
        more_base_patterns1 = [
            swap_substrings(s, subs1=answer, subs2=distractor).replace("más", "menos")
            for s in base_patterns
            if "más" in s
        ]
        base_patterns.extend(more_base_patterns1)

        # replace longer with shorter and swap answer and distractor
        more_base_patterns2 = [
            swap_substrings(s, subs1=answer, subs2=distractor).replace("larga", "corta")
            for s in base_patterns
            if "larga" in s
        ]
        base_patterns.extend(more_base_patterns2)

        return base_patterns + self.get_shared_patterns(target=answer)

    def negative_scorer(self, prediction, answer, distractor, diff):
        score, certainty = None, None

        negative_patterns = [
            distractor,
            rf"{distractor} tiene más letras",
            rf"{distractor} tiene más letras que {answer}",
            rf"{distractor} tiene {diff} letra(s)? más",
            rf"{distractor} tiene {diff} letra(s)? más que {answer}",
            rf"La palabra con más letras es {distractor}",
            rf"{distractor} es la palabra que tiene más letras",
            rf"{distractor} es más larga",
            rf"{distractor} es más larga por {diff} letra(s)?",
            rf"{distractor} es más larga que {answer}",
            rf"{distractor} es más larga que {answer} por {diff} letra(s)?",
            rf"La palabra más larga es {distractor}",
            rf"{distractor} es la palabra más larga",
        ]
        for negative_pattern in negative_patterns:
            negative_pattern = self.normalize_string(negative_pattern)
            if re.match(rf"{negative_pattern}\.?$", prediction):
                score = 0
                certainty = 1
                break

        # the model correctly picks the longer word, but wrongly states the difference in letters:
        number_regex = r"(?P<number>\d+|una|dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez|cero|una sola)"
        wrong_diff_patterns = [
            rf"{answer} tiene {number_regex} letra(s)? más",
            rf"{answer} tiene {number_regex} letra(s)? más que {distractor}",
            rf"{answer} es más larga por {number_regex} letra(s)?",
            rf"{answer} es más larga que {distractor} por {number_regex} letra(s)?",
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
        diff = len(answer) - len(distractor)
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
