import re

from lmentry.scorers.en.scorer import (
    LMentryScorer, swap_substrings, the_word_regex, standardized_number_regex
)


class MoreLettersScorer(LMentryScorer):

    def __init__(self):
        super().__init__()

        self.prefixes.extend([
            "Von den Wörtern {word1} und {word2}, ",
            "Zwischen den Wörtern {word1} und {word2}, ",
        ])

    def get_base_patterns(self, answer, distractor, diff):

        longer = r"(länger)"
        base_patterns = [
            rf"{answer} hat mehr Buchstaben",
            rf"{answer} hat mehr Buchstaben als {distractor}",
            rf"{answer} hat {diff} Buchstaben mehr",
            rf"{answer} hat {diff} Buchstaben mehr als {distractor}",
            rf"Das Wort, das mehr Buchstaben hat, ist {answer}",
            rf"{answer} ist das Wort, das mehr Buchstaben hat",
            rf"{answer} ist {longer}",
            rf"{answer} ist {longer} als {distractor}",
            rf"{answer} ist {diff} Buchstaben {longer} als {distractor}",
            rf"Das {longer}e Wort ist {answer}",
            rf"Das Wort, das {longer} ist, ist {answer}",
            rf"{answer} ist das Wort, das {longer} ist",
            rf"{answer} ist das {longer}e Wort",
        ]
        # replace more with less or fewer and swap answer and distractor
        less = r"(weniger)"
        more_base_patterns1 = [
            swap_substrings(s, subs1=answer, subs2=distractor).replace("mehr", less)
            for s in base_patterns
            if "mehr" in s
        ]
        base_patterns.extend(more_base_patterns1)

        # replace longer with shorter and swap answer and distractor
         
        more_base_patterns2 = [
            swap_substrings(s, subs1=answer, subs2=distractor).replace(longer, "kürzer")
            for s in base_patterns
            if longer in s
        ]
        base_patterns.extend(more_base_patterns2)

        return base_patterns + self.get_shared_patterns(target=answer)

    def negative_scorer(self, prediction, answer, distractor, diff):
        score, certainty = None, None

        longer = r"(länger)"
        negative_patterns = [
            distractor,
            rf"{distractor} hat mehr Buchstaben",
            rf"{distractor} hat mehr Buchstaben als {answer}",
            rf"{distractor} hat {diff} Buchstaben mehr",
            rf"{distractor} hat {diff} Buchstaben mehr als {answer}",
            rf"Das Wort, das mehr Buchstaben hat, ist {distractor}",
            rf"{distractor} ist das Wort, das mehr Buchstaben hat",
            rf"{distractor} ist {longer}",
            rf"{distractor} ist {diff} Buchstaben {longer}",
            rf"{distractor} ist {longer} als {answer}",
            rf"{distractor} ist {diff} Buchstaben {longer} als {answer}",
            rf"Das {longer}e Wort ist {distractor}",
            rf"Das Wort, das {longer} ist, ist {distractor}",
            rf"{distractor} ist das Wort, das {longer} ist",
            rf"{distractor} ist das {longer}e Wort",
        ]
        for negative_pattern in negative_patterns:
            negative_pattern = self.normalize_string(negative_pattern)
            if re.match(rf"{negative_pattern}\.?$", prediction):
                score = 0
                certainty = 1
                break

        # the model correctly picks the longer word, but wrongly states the difference in letters:
        number_regex = r"(?P<number>\d+|einen|zwei|drei|vier|fünf|sechs|sieben|acht|neun|zehn|null|einen einzigen)"
        wrong_diff_patterns = [
            rf"{answer} hat {number_regex} Buchstaben mehr",
            rf"{answer} hat {number_regex} Buchstaben mehr als {distractor}",
            rf"{answer} ist {number_regex} Buchstaben länger",
            rf"{answer} ist {number_regex} Buchstaben länger als {distractor}",
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
