import re

from lmentry.scorers.es.scorer import (
    LMentryScorer, swap_substrings, the_word_regex, standardized_number_regex
)


class LessLettersScorer(LMentryScorer):
    """This class was created by simply mirroring `MoreLettersScorer`
    """
    def __init__(self):
        super().__init__()

        self.prefixes.extend([
            "De las palabras {word1} y {word2}, ",
            "Entre las palabras {word1} y {word2}, ",
        ])

    def get_base_patterns(self, answer, distractor, diff):

        base_patterns = [
            rf"{answer} tiene menos letras",
            rf"{answer} tiene menos letras que {distractor}",
            rf"{answer} tiene {diff} letra(s)? menos",
            rf"{answer} tiene {diff} letra(s)? menos que {distractor}",
            rf"La palabra que tiene menos letras es {answer}",
            rf"{answer} es la palabra con menos letras",
            rf"{answer} es más corta",
            rf"{answer} es más corta que {distractor}",
            rf"{answer} es más corta que {distractor} por {diff} letra(s)?",
            rf"La palabra más corta es {answer}",
            rf"{answer} es la palabra más corta",
        ]
        # replace less with more and swap answer and distractor
        more_base_patterns1 = [
            swap_substrings(s, subs1=answer, subs2=distractor).replace("menos", "más")
            for s in base_patterns
            if "menos" in s
        ]
        base_patterns.extend(more_base_patterns1)

        # replace shorter with longer and swap answer and distractor
        more_base_patterns2 = [
            swap_substrings(s, subs1=answer, subs2=distractor).replace("corta", "larga")
            for s in base_patterns
            if "corta" in s
        ]
        base_patterns.extend(more_base_patterns2)

        return base_patterns + self.get_shared_patterns(target=answer)
    
    def negative_scorer(self, prediction, answer, distractor, diff):
        score, certainty = None, None

        negative_patterns = [
            distractor,
            rf"{distractor} tiene menos letras",
            rf"{distractor} tiene menos letras que {answer}",
            rf"{distractor} tiene {diff} letra(s)? menos",
            rf"{distractor} tiene {diff} letra(s)? menos que {answer}",
            rf"La palabra con menos letras es {distractor}",
            rf"{distractor} es la palabra que tiene menos letras",
            rf"{distractor} es más corta",
            rf"{distractor} es más corta por {diff} letra(s)?",
            rf"{distractor} es más corta que {answer}",
            rf"{distractor} es más corta que {answer} por {diff} letra(s)?",
            rf"La palabra más corta es {distractor}",
            rf"{distractor} es la palabra más corta",
        ]
        for negative_pattern in negative_patterns:
            negative_pattern = self.normalize_string(negative_pattern)
            if re.match(rf"{negative_pattern}\.?$", prediction):
                score = 0
                certainty = 1
                break

        # the model correctly picks the shorter word, but wrongly states the difference in letters:
        number_regex = r"(?P<number>\d+|una|dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez|cero|una sola)"
        wrong_diff_patterns = [
            rf"{answer} tiene {number_regex} letra(s)? menos",
            rf"{answer} tiene {number_regex} letra(s)? menos que {distractor}",
            rf"{answer} es más corta por {number_regex} letra(s)?",
            rf"{answer} es más corta que {distractor} por {number_regex} letra(s)?",
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
