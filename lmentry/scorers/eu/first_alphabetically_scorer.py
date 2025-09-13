import re

from lmentry.scorers.eu.scorer import LMentryScorer, the_word_regex


class FirstAlphabeticallyScorer(LMentryScorer):
    def __init__(self):
        super().__init__()

        # "Q: Alfabetikoki, zein hitz dator lehenago: \"{word1}\" edo \"{word2}\"?\nA:"
        # "Q: Alfabetoaren araberako hurrenkeran, zein hitz dator lehenago, \"{word1}\" edo \"{word2}\"?\nA:"
        # "Q: \"{word1}\" eta \"{word2}\" hitzen artean, zein dator lehenago ordena alfabetikoan?\nA:"

        self.prefixes.extend([
            r"Alfabetikoki,? ",
            r"Alfabetoaren araberako hurrenkeran,? ",
            r"Hurrenkera alfabetikoan,? ",
            r"Ordena alfabetikoan,? ",
            r"\"?{word1}\"? eta \"?{word2}\"? hitzen artean,? ",
            r"\"?{word1}\"? eta \"?{word2}\"? hitzetatik,? ",
            r"Hitz (hauetatik|horietatik),? ",
        ])

        self.suffixes.extend([
            " alfabetikoki",
            " alfabetoaren araberako hurrenkeran",
            " hurrenkera alfabetikoan",
            " ordena alfabetikoan",
        ])

    def get_base_patterns(self, answer, distractor):

        earlier = r"(lehenago|lehenengo|lehenik)"
        later = r"(gero|geroago)"
        comes = "(dator|dago|doa)"

        base_patterns = [
            rf"{answer} {comes} {earlier}",
            rf"{answer} {earlier} {comes}",
            rf"{answer} {comes} {earlier}",
            rf"{answer} {earlier} {comes}",
            rf"{distractor} {comes} bigarren",
            rf"{distractor} bigarren {comes}",
            rf"{distractor} {comes} {later}",
            rf"{distractor} {later} {comes}",
            rf"{answer} {comes} {distractor} baino lehen",
            rf"{answer} {distractor} baino lehen {comes}",
            rf"{distractor} {comes} {answer} eta gero",
            rf"{distractor} {answer} eta gero {comes}",
        ]
        return base_patterns + self.get_shared_patterns(target=answer)

    def get_exact_patterns(self, answer):
        return [
            rf"\"?{answer}\"?"
        ]

    def negative_scorer(self, prediction, answer):
        score, certainty = None, None

        predictions_words = re.findall(r"\b[a-z]+\b", prediction)
        if len(predictions_words) == 1 and predictions_words[0] != answer:
            score = 0
            certainty = 1

        return score, certainty

    def score_prediction(self, prediction, example, truncate_prediction: bool = False):
        prediction = self.normalize_prediction(prediction, truncate_prediction)

        metadata = example["metadata"]
        answer = metadata["answer"]
        score, certainty = self.negative_scorer(prediction, answer)
        if score is not None:
            return score, certainty

        distractor = metadata["distractor"]
        word1 = metadata["word1"]
        word2 = metadata["word2"]

        answer = the_word_regex(answer)
        distractor = the_word_regex(distractor)

        exact_patterns = self.get_exact_patterns(answer)
        for exact_pattern in exact_patterns:
            score, certainty = self._simple_scorer(prediction, answer=exact_pattern)
            if score:
                return score, certainty

        base_patterns = self.get_base_patterns(answer, distractor)
        self.prefix_kwargs = {"word1": word1, "word2": word2}

        score, certainty = self.certainty_scorer(prediction, base_patterns)
        return score, certainty
