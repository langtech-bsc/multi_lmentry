import re

from lmentry.scorers.pt_br.scorer import (
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
            rf"{answer} tem mais",
            rf"{answer} tem mais letras que {distractor}",
            rf"{answer} tem {diff} letra(s)? a mais",
            rf"{answer} tem {diff} letra(s)? a mais que {distractor}",
            rf"{answer} é {diff} letra(s)? (mais longa|maior) que {distractor}",
            rf"A palavra que tem mais letras é {answer}",
            rf"{answer} é a palavra com mais letras",
            rf"{answer} é (mais longa|maior)",
            rf"{answer} é (mais longa|maior) que {distractor}",
            rf"{answer} é (mais longa|maior) que {distractor} por {diff} letra(s)?",
            rf"A palavra (mais longa|maior) é {answer}",
            rf"{answer} é a palavra (mais longa|maior)",
        ]

        # replace more with less or fewer and swap answer and distractor
        more_base_patterns1 = [
            swap_substrings(s, subs1=answer, subs2=distractor).replace("mais", "menos")
            for s in base_patterns
            if "mais" in s
        ]
        base_patterns.extend(more_base_patterns1)

        # replace longer with shorter and swap answer and distractor
        more_base_patterns2 = [
            swap_substrings(s, subs1=answer, subs2=distractor).replace("longa", "curta")
            for s in base_patterns
            if "longa" in s
        ]
        base_patterns.extend(more_base_patterns2)

        return base_patterns + self.get_shared_patterns(target=answer)

    def negative_scorer(self, prediction, answer, distractor, diff):
        score, certainty = None, None

        negative_patterns = [
            distractor,
            rf"{distractor} tem mais letras",
            rf"{distractor} tem mais letras {answer}",
            rf"{distractor} tem {diff} letra(s)? a mais",
            rf"{distractor} tem {diff} letra(s)? a mais que {answer}",
            rf"A palavra com mais letras é {distractor}",
            rf"{distractor} é a (palavra)? que tem mais letras",
            rf"{distractor} é (mais longa|maior)",
            rf"{distractor} é (mais curta|menor) por {diff} letra(s)?",
            rf"{distractor} é (mais longa|maior) que {answer}",
            rf"{distractor} é (mais longa|maior) que {answer} por {diff} letra(s)?",
            rf"{distractor} é {diff} letra(s)? (mais longa|maior) que {answer}",
            rf"A palavra (mais longa|maior) é {distractor}",
            rf"{distractor} é a palavra (mais longa|maior)",
        ]

        for negative_pattern in negative_patterns:
            negative_pattern = self.normalize_string(negative_pattern)
            if re.match(rf"{negative_pattern}\.?$", prediction):
                score = 0
                certainty = 1
                break

        # the model correctly picks the longer word, but wrongly states the difference in letters:
        number_regex = r"(?P<number>\d+|uma|duas|três|quatro|cinco|seis|sete|oito|nove|dez|zero|uma só|só uma)"
        wrong_diff_patterns = [
            rf"{answer} tem {number_regex} letra(s)? a mais",
            rf"{answer} tem {number_regex} letra(s)? a mais que {distractor}",
            rf"{answer} é (mais longa|maior) por {number_regex} letra(s)?",
            rf"{answer} é {number_regex} letra(s) (mais longa|maior)",
            rf"{answer} é (mais longa|maior) que {distractor} por {number_regex} letra(s)?",
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
