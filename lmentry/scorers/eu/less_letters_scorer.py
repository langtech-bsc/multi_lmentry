import re

from lmentry.scorers.eu.scorer import (
    LMentryScorer, swap_substrings, the_word_regex, standardized_number_regex
)


class LessLettersScorer(LMentryScorer):
    """This class was created by simply mirroring `MoreLettersScorer`
    """
    def __init__(self):
        super().__init__()

        # 'Q: Zein hitzek du letra gutxiago, "{word1}" edo "{word2}"?\nA:'
        # 'Q: Zein hitz da laburragoa, "{word1}" edo "{word2}"?\nA:'
        # 'Q: "{word1}" eta "{word2}" hitzen artean, zeinek du letra gutxiago?\nA:'

        self.prefixes.extend([
            r"\"?{word1}\"? eta \"?{word2}\"? hitzen artean,? ",
            r"Hitz (hauen|horien) artean,? ",
        ])

    def get_base_patterns(self, answer, distractor, diff):

        answer = rf"\"?{answer}\"?"
        distractor = rf"\"?{distractor}\"?"

        less = r"gutxiago"
        least = r"gutxien"
        shorter = r"(laburragoa|motzagoa)"
        shortest = r"(laburrena|motzena)"
        has = r"(du|dauka|ditu|dauzka)"
        that_has = r"(duen|daukan|dituen|dauzkan)"
        the_one_the_has = r"(duena|daukana|dituena|dauzkana)"

        base_patterns = [
            rf"{answer} hitzak?",
            rf"{answer}( hitza)? ({shortest}|{shorter}) da",
            rf"{answer}( hitza)? da ({shortest}|{shorter})",
            rf"{answer}( hitza)? hitzik {shortest} da",
            rf"{answer}( hitza)? da hitzik {shortest}",
            rf"{answer} hitzak {has} letra ({less}|{least})",
            rf"{answer} hitzak letra ({less}|{least}) {has}",
            rf"Letra ({less}|{least}) {that_has} hitza {answer} da",
            rf"Letra ({less}|{least}) {the_one_the_has} {answer} da",
            rf"{answer} da letra ({less}|{least}) {the_one_the_has}",
            rf"{answer} da letra ({less}|{least}) {that_has} hitza",
            rf"{answer} hitzak {distractor}( hitzak)? baino letra {less} {has}",
            rf"{answer} hitzak {distractor}( hitzak)? baino {diff} letra {less} {has}",
            rf"{answer} hitzak {distractor}( hitzak)? baino letra {diff} {less} {has}",
            rf"Hitzik {shortest} {answer} da"
            rf"{answer} {distractor} baino {shorter} da",
            rf"{answer} {distractor} baino {diff} letra {shorter} da",
            rf"{answer} {distractor} baino letra {diff} {shorter} da",
        ]
        # replace less with more and swap answer and distractor
        more_base_patterns1 = [
            swap_substrings(s, subs1=answer, subs2=distractor).replace(less, "gehiago").replace(least, "gehien")
            for s in base_patterns
            if less in s or least in s
        ]
        base_patterns.extend(more_base_patterns1)

        # replace shorter with longer and swap answer and distractor
        more_base_patterns2 = [
            swap_substrings(s, subs1=answer, subs2=distractor).replace(shorter, "luzeagoa").replace(shortest, "luzeena")
            for s in base_patterns
            if shorter in s or shortest in s
        ]
        base_patterns.extend(more_base_patterns2)

        return base_patterns + self.get_shared_patterns(target=answer)
    
    def negative_scorer(self, prediction, answer, distractor, diff):
        score, certainty = None, None

        answer = rf"\"?{answer}\"?"
        distractor = rf"\"?{distractor}\"?"

        less = r"gutxiago"
        least = r"gutxien"
        shorter = r"(laburragoa|motzagoa)"
        shortest = r"(laburrena|motzena)"
        has = r"(du|dauka|ditu|dauzka)"
        that_has = r"(duen|daukan|dituen|dauzkan)"
        the_one_the_has = r"(duena|daukana|dituena|dauzkana)"

        negative_patterns = [
            rf"{distractor} hitzak?",
            rf"{distractor}( hitza)? ({shortest}|{shorter}) da",
            rf"{distractor}( hitza)? da ({shortest}|{shorter})",
            rf"{distractor}( hitza)? hitzik {shortest} da",
            rf"{distractor}( hitza)? da hitzik {shortest}",
            rf"{distractor} hitzak {has} letra ({less}|{least})",
            rf"Letra ({less}|{least}) {that_has} hitza {distractor} da",
            rf"Letra ({less}|{least}) {the_one_the_has} {distractor} da",
            rf"{distractor} da letra ({less}|{least}) {the_one_the_has}",
            rf"{distractor} da letra ({less}|{least}) {that_has} hitza",
            rf"{distractor} hitzak {answer}( hitzak)? baino letra {less} {has}",
            rf"{distractor} hitzak {answer}( hitzak)? baino {diff} letra {less} {has}",
            rf"{distractor} hitzak {answer}( hitzak)? baino letra {diff} {less} {has}",
            rf"Hitzik {shortest} {distractor} da"
            rf"{distractor} {answer} baino {shorter} da",
            rf"{distractor} {answer} baino {diff} letra {shorter} da",
            rf"{distractor} {answer} baino letra {diff} {shorter} da",
        ]
        for negative_pattern in negative_patterns:
            negative_pattern = self.normalize_string(negative_pattern)
            if re.match(rf"{negative_pattern}\.?$", prediction):
                score = 0
                certainty = 1
                break

        # the model correctly picks the shorter word, but wrongly states the difference in letters:
        number_regex = r"(?P<number>\d+|bat|bi|hiru|lau|bost|sei|zazpi|zortzi|bederatzi|hamar)"
        wrong_diff_patterns = [
            rf"{answer} hitzak {distractor}( hitzak)? baino {number_regex} letra {less} ditu",
            rf"{answer} hitzak {distractor}( hitzak)? baino letra {number_regex} {less} ditu",
            rf"{answer} {distractor} baino {number_regex} letra {shorter} da",
            rf"{answer} {distractor} baino letra {number_regex} {shorter} da",
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

        diff = standardized_number_regex(diff)

        score, certainty = self.negative_scorer(prediction, answer, distractor, diff)
        if score is not None:
            return score, certainty

        score, certainty = self._simple_scorer(prediction, the_word_regex(answer))
        if score:
            return score, certainty

        base_patterns = self.get_base_patterns(answer, distractor, diff)
        self.prefix_kwargs = {"word1": word1, "word2": word2}

        score, certainty = self.certainty_scorer(prediction, base_patterns)
        return score, certainty
