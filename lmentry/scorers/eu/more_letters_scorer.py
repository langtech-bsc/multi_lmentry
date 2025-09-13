import re

from lmentry.scorers.eu.scorer import (
    LMentryScorer, swap_substrings, the_word_regex, standardized_number_regex
)


class MoreLettersScorer(LMentryScorer):

    def __init__(self):
        super().__init__()

        # 'Q: Zein hitzek du letra gehiago, "{word1}" edo "{word2}"?\nA:'
        # 'Q: Zein hitz da luzeagoa, "{word1}" edo "{word2}"?\nA:'
        # 'Q: "{word1}" eta "{word2}" hitzen artean, zeinek du letra gehiago?\nA:'

        self.prefixes.extend([
            r"\"?{word1}\"? eta \"?{word2}\"? hitzen artean,? ",
            r"Hitz (hauen|horien) artean,? ",
        ])

    def get_base_patterns(self, answer, distractor, diff):

        answer = rf"\"?{answer}\"?"
        distractor = rf"\"?{distractor}\"?"

        more = r"gehiago"
        most = r"gehien"
        longer = r"luzeagoa"
        longest = r"luzeena"
        has = r"(du|dauka|ditu|dauzka)"
        that_has = r"(duen|daukan|dituen|dauzkan)"
        the_one_the_has = r"(duena|daukana|dituena|dauzkana)"

        base_patterns = [
            rf"{answer} hitzak?",
            rf"{answer}( hitza)? ({longest}|{longer}) da",
            rf"{answer}( hitza)? da ({longest}|{longer})",
            rf"{answer}( hitza)? hitzik {longest} da",
            rf"{answer}( hitza)? da hitzik {longest}",
            rf"{answer} hitzak {has} letra ({more}|{most})",
            rf"{answer} hitzak letra ({more}|{most}) {has}",
            rf"Letra ({more}|{most}) {that_has} hitza {answer} da",
            rf"Letra ({more}|{most}) {the_one_the_has} {answer} da",
            rf"{answer} da letra ({more}|{most}) {the_one_the_has}",
            rf"{answer} da letra ({more}|{most}) {that_has} hitza",
            rf"{answer} hitzak {distractor}( hitzak)? baino letra {more} {has}",
            rf"{answer} hitzak {distractor}( hitzak)? baino {diff} letra {more} {has}",
            rf"{answer} hitzak {distractor}( hitzak)? baino letra {diff} {more} {has}",
            rf"Hitzik {longest} {answer} da"
            rf"{answer} {distractor} baino {longer} da",
            rf"{answer} {distractor} baino {diff} letra {longer} da",
        ]
        # replace more with less or fewer and swap answer and distractor
        more_base_patterns1 = [
            swap_substrings(s, subs1=answer, subs2=distractor).replace(more, "gutxiago").replace(most, "gutxien")
            for s in base_patterns
            if more in s or most in s
        ]
        base_patterns.extend(more_base_patterns1)

        # replace longer with shorter and swap answer and distractor
        more_base_patterns2 = [
            swap_substrings(s, subs1=answer, subs2=distractor).replace(longer, "(laburragoa|motzagoa)").replace(longest, "(laburrena|motzena)")
            for s in base_patterns
            if longer in s or longest in s
        ]
        base_patterns.extend(more_base_patterns2)

        return base_patterns + self.get_shared_patterns(target=answer)

    def negative_scorer(self, prediction, answer, distractor, diff):
        score, certainty = None, None

        answer = rf"\"?{answer}\"?"
        distractor = rf"\"?{distractor}\"?"

        more = r"gehiago"
        most = r"gehien"
        longer = r"luzeagoa"
        longest = r"luzeena"
        has = r"(du|dauka|ditu|dauzka)"
        that_has = r"(duen|daukan|dituen|dauzkan)"
        the_one_the_has = r"(duena|daukana|dituena|dauzkana)"

        negative_patterns = [
            rf"{distractor} hitzak?",
            rf"{distractor}( hitza)? ({longest}|{longer}) da",
            rf"{distractor}( hitza)? da ({longest}|{longer})",
            rf"{distractor}( hitza)? hitzik {longest} da",
            rf"{distractor}( hitza)? da hitzik {longest}",
            rf"{distractor} hitzak {has} letra ({more}|{most})",
            rf"Letra ({more}|{most}) {that_has} hitza {distractor} da",
            rf"Letra ({more}|{most}) {the_one_the_has} {distractor} da",
            rf"{distractor} da letra ({more}|{most}) {the_one_the_has}",
            rf"{distractor} da letra ({more}|{most}) {that_has} hitza",
            rf"{distractor} hitzak {answer}( hitzak)? baino letra {more} {has}",
            rf"{distractor} hitzak {answer}( hitzak)? baino {diff} letra {more} {has}",
            rf"{distractor} hitzak {answer}( hitzak)? baino letra {diff} {more} {has}",
            rf"Hitzik {longest} {distractor} da"
            rf"{distractor} {answer} baino {longer} da",
            rf"{distractor} {answer} baino {diff} letra {longer} da",
            rf"{distractor} {answer} baino letra {diff} {longer} da",
        ]
        for negative_pattern in negative_patterns:
            negative_pattern = self.normalize_string(negative_pattern)
            if re.match(rf"{negative_pattern}\.?$", prediction):
                score = 0
                certainty = 1
                break

        # the model correctly picks the longer word, but wrongly states the difference in letters:
        number_regex = r"(?P<number>\d+|one|two|three|four|five|six|seven|eight|nine|ten|zero|a single)"
        wrong_diff_patterns = [
            rf"{answer} hitzak {distractor}( hitzak)? baino {number_regex} letra {more} ditu",
            rf"{answer} hitzak {distractor}( hitzak)? baino letra {number_regex} {more} ditu",
            rf"{answer} {distractor} baino {number_regex} letra {longer} da",
            rf"{answer} {distractor} baino letra {number_regex} {longer} da",
        ]
        for wrong_diff_pattern in wrong_diff_patterns:
            if res := re.match(wrong_diff_pattern, prediction):
                predicted_diff = res.group("number")  # todo: no standardized_number_regex?
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
