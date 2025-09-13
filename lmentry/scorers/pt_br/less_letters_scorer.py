import re

from lmentry.scorers.pt_br.scorer import (
    LMentryScorer, swap_substrings, the_word_regex, standardized_number_regex
)


class LessLettersScorer(LMentryScorer):
    """This class was created by simply mirroring `MoreLettersScorer`
    """
    def __init__(self):
        super().__init__()

        self.prefixes.extend([
            "Das palavras {word1} e {word2}, ",
            "Entre as palavras {word1} e {word2}, ",
            "Dentre as palavras {word1} e {word2}, ",
        ])

    def get_base_patterns(self, answer, distractor, diff):

        base_patterns = [
            rf"{answer} tem menos",
            rf"{answer} tem menos letras que {distractor}",
            rf"{answer} tem {diff} letra(s)? a menos",
            rf"{answer} tem {diff} letra(s)? a menos que {distractor}",
            rf"{answer} é {diff} letra(s)? (mais curta|menor) que {distractor}",
            rf"A palavra que tem menos letras é {answer}",
            rf"{answer} é a palavra com menos letras",
            rf"{answer} é (mais curta|menor)",
            rf"{answer} é (mais curta|menor) que {distractor}",
            rf"{answer} é (mais curta|menor) que {distractor} por {diff} letra(s)?",
            rf"A palavra (mais curta|menor) é {answer}",
            rf"{answer} é a palavra (mais curta|menor)",
        ]
        # replace less with more and swap answer and distractor
        more_base_patterns1 = [
            swap_substrings(s, subs1=answer, subs2=distractor).replace("menos", "mais")
            for s in base_patterns
            if "menos" in s
        ]
        base_patterns.extend(more_base_patterns1)

        # replace shorter with longer and swap answer and distractor
        more_base_patterns2 = [
            swap_substrings(s, subs1=answer, subs2=distractor).replace("curta", "longa")
            for s in base_patterns
            if "curta" in s
        ]
        base_patterns.extend(more_base_patterns2)

        return base_patterns + self.get_shared_patterns(target=answer)
    
    def negative_scorer(self, prediction, answer, distractor, diff):
        score, certainty = None, None

        negative_patterns = [
            distractor,
            rf"{distractor} tem menos letras",
            rf"{distractor} tem menos letras {answer}",
            rf"{distractor} tem {diff} letra(s)? a menos",
            rf"{distractor} tem {diff} letra(s)? a menos que {answer}",
            rf"A palavra com menos letras é {distractor}",
            rf"{distractor} é a (palavra)? que tem menos letras",
            rf"{distractor} é (mais curta|menor)",
            rf"{distractor} é (mais curta|menor) por {diff} letra(s)?",
            rf"{distractor} é (mais curta|menor) que {answer}",
            rf"{distractor} é (mais curta|menor) que {answer} por {diff} letra(s)?",
            rf"{distractor} é {diff} letra(s)? (mais curta|menor) que {answer}",
            rf"A palavra (mais curta|menor) é {distractor}",
            rf"{distractor} é a palavra (mais curta|menor)",
        ]

        for negative_pattern in negative_patterns:
            negative_pattern = self.normalize_string(negative_pattern)
            if re.match(rf"{negative_pattern}\.?$", prediction):
                score = 0
                certainty = 1
                break

        # the model correctly picks the shorter word, but wrongly states the difference in letters:
        number_regex = r"(?P<number>\d+|uma|duas|três|quatro|cinco|seis|sete|oito|nove|dez|zero|uma só|só uma)"
        wrong_diff_patterns = [
            rf"{answer} tem {number_regex} letra(s)? a menos",
            rf"{answer} tem {number_regex} letra(s)? a menos que {distractor}",
            rf"{answer} é (mais curta|menor) por {number_regex} letra(s)?",
            rf"{answer} é {number_regex} letra(s) (mais curta|menor)",
            rf"{answer} é (mais curta|menor) que {distractor} por {number_regex} letra(s)?",
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
