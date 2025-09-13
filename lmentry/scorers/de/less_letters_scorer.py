import re

from lmentry.scorers.en.scorer import (
    LMentryScorer, swap_substrings, the_word_regex, standardized_number_regex
)


class LessLettersScorer(LMentryScorer):
    """This class was created by simply mirroring `MoreLettersScorer`
    """
    def __init__(self):
        super().__init__()

        self.prefixes.extend([
            "Von den Wörtern {word1} und {word2}, ",
            "Zwischen den Wörtern {word1} und {word2}, ",
        ])

    def get_base_patterns(self, answer, distractor, diff):

        less = r"(weniger)"
        shorter = r"(kürzer)"
        base_patterns = [
            rf"{answer} hat {less} Buchstaben",
            rf"{answer} hat {less} Buchstaben als {distractor}",
            rf"{answer} hat {diff} Buchstaben {less}",
            rf"{answer} hat {diff} Buchstaben {less} als {distractor}",
            rf"Das Wort, das {less} Buchstaben hat, ist {answer}",
            rf"{answer} ist das Wort, das {less} Buchstaben hat",
            rf"{answer} ist das Wort mit {less} Buchstaben",
            rf"{answer} ist {shorter}",
            rf"{answer} ist {shorter} als {distractor}",
            rf"{answer} ist {diff} Buchstaben {shorter} als {distractor}",
            rf"Das {shorter}e Wort ist {answer}",
            rf"Das Wort, das {shorter} ist, ist {answer}",
            rf"{answer} ist das Wort, das {shorter} ist",
            rf"{answer} ist das {shorter}e Wort",
        ]
        # replace less with more and swap answer and distractor
        more_base_patterns1 = [
            swap_substrings(s, subs1=answer, subs2=distractor).replace(less, "mehr")
            for s in base_patterns
            if less in s
        ]
        base_patterns.extend(more_base_patterns1)

        # replace shorter with longer and swap answer and distractor
        more_base_patterns2 = [
            swap_substrings(s, subs1=answer, subs2=distractor).replace(shorter, "länger")
            for s in base_patterns
            if shorter in s
        ]
        base_patterns.extend(more_base_patterns2)

        return base_patterns + self.get_shared_patterns(target=answer)
    
    def negative_scorer(self, prediction, answer, distractor, diff):
        score, certainty = None, None

        less = r"(weniger)"
        shorter = r"(kürzer)"
        negative_patterns = [
            distractor,
            rf"{distractor} hat {less} Buchstaben",
            rf"{distractor} hat {less} Buchstaben als {answer}",
            rf"{distractor} hat {diff} {less} Buchstaben?",
            rf"{distractor} hat {diff} {less} Buchstaben als {answer}",
            rf"Das Wort, das {less} Buchstaben hat, ist {distractor}",
            rf"{distractor} ist das Wort, das {less} Buchstaben hat",
            rf"{distractor} ist das Wort mit {less} Buchstaben",
            rf"{distractor} ist {shorter}",
            rf"{distractor} ist {diff} Buchstaben {shorter}",
            rf"{distractor} ist {shorter} als {answer}",
            rf"{distractor} ist {diff} Buchstaben {shorter} als {answer}",
            rf"Das {shorter}e Wort ist {distractor}",
            rf"Das Wort, das {shorter} ist, ist {distractor}",
            rf"{distractor} ist das Wort, das {shorter} ist",
            rf"{distractor} ist das {shorter}e Wort",
        ]
        for negative_pattern in negative_patterns:
            negative_pattern = self.normalize_string(negative_pattern)
            if re.match(rf"{negative_pattern}\.?$", prediction):
                score = 0
                certainty = 1
                break

        # the model correctly picks the shorter word, but wrongly states the difference in letters:
        number_regex = r"(?P<number>\d+|einen|zwei|drei|vier|fünf|sechs|sieben|acht|neun|zehn|null|einen einzigen)"
        wrong_diff_patterns = [
            rf"{answer} hat {number_regex} Buchstaben {less}",
            rf"{answer} hat {number_regex} Buchstaben {less} als {distractor}",
            rf"{answer} ist um {number_regex} Buchstaben kürzer",
            rf"{answer} ist um {number_regex} Buchstaben kürzer als {distractor}",
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
