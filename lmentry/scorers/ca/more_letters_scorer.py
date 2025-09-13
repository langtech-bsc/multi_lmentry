import re

from lmentry.scorers.ca.scorer import (
    LMentryScorer, swap_substrings, the_word_regex, standardized_number_regex
)


class MoreLettersScorer(LMentryScorer):

    def __init__(self):
        super().__init__()

        self.prefixes.extend([
            "De les paraules {word1} i {word2}, ",
            "Entre les paraules {word1} i {word2}, ",
        ])

    def get_base_patterns(self, answer, distractor, diff):

        letter = r"(lletra|lletres)"
        base_patterns = [
            rf"{answer} té més lletres",
            rf"{answer} té més lletres que {distractor}",
            rf"{answer} té {diff} {letter} més",
            rf"{answer} té {diff} {letter} més que {distractor}",
            rf"La paraula que té més lletres és {answer}",
            rf"{answer} és la paraula que té més lletres",
            rf"{answer} és la paraula més llarga",
            rf"{answer} és més llarga que {distractor}",
            rf"{answer} és més llarga que {distractor} per una diferència de {diff} {letter}",
            rf"La paraula més llarga és {answer}",
        ]
        # replace more with less or fewer and swap answer and distractor
        more_base_patterns1 = [
            swap_substrings(s, subs1=answer, subs2=distractor).replace("més", "menys")
            for s in base_patterns
            if "més" in s
        ]
        base_patterns.extend(more_base_patterns1)

        # replace longer with shorter and swap answer and distractor
        more_base_patterns2 = [
            swap_substrings(s, subs1=answer, subs2=distractor).replace("llarga", "curta")
            for s in base_patterns
            if "llarga" in s
        ]
        base_patterns.extend(more_base_patterns2)

        return base_patterns + self.get_shared_patterns(target=answer)

    def negative_scorer(self, prediction, answer, distractor, diff):
        score, certainty = None, None

        letter = r"(lletra|lletres)"
        negative_patterns = [
            distractor,
            rf"{distractor} té més lletres",
            rf"{distractor} té més lletres que {answer}",
            rf"{distractor} té {diff} {letter} més",
            rf"{distractor} té {diff} {letter} més que {answer}",
            rf"La paraula que té més lletres és {distractor}",
            rf"{distractor} és la paraula que té més lletres",
            rf"{distractor} és la paraula més llarga",
            rf"{distractor} és més llarga per {diff} {letter}",
            rf"{distractor} és més llarga que {answer}",
            rf"{distractor} és més llarga que {answer} per una diferència de {diff} {letter}",
            rf"La paraula més llarga és {distractor}",
        ]
        for negative_pattern in negative_patterns:
            negative_pattern = self.normalize_string(negative_pattern)
            if re.match(rf"{negative_pattern}\.?$", prediction):
                score = 0
                certainty = 1
                break

        # the model correctly picks the longer word, but wrongly states the difference in letters:
        number_regex = r"(?P<number>\d+|una|dues|tres|quatre|cinc|sis|set|vuit|nou|deu|zero|una sola)"
        wrong_diff_patterns = [
            rf"{answer} té {number_regex} {letter} més",
            rf"{answer} té {number_regex} {letter} més que {distractor}",
            rf"{answer} és més llarga per {number_regex} {letter}",
            rf"{answer} és més llarga que {distractor} per una diferència de {number_regex} {letter}",
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
