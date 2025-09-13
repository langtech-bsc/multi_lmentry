import re

from lmentry.scorers.en.scorer import LMentryScorer, the_word_regex, the_words_regex, swap_substrings


class MostAssociatedWordScorer(LMentryScorer):
    def __init__(self):
        super().__init__()

        # we use `[^a-zA-Z0-9_]` instead of `\W` as we always lowercase the pattern in
        # `certainty_scorer`. See the to-do suggestion in normalize_string

        self.prefixes.extend([
            r"{words}[^a-zA-Z0-9_]*"
        ])

        self.suffixes.extend([
            r"[^a-zA-Z0-9_]*{words}"
        ])

    def get_base_patterns(self, answer, category, words):

        to_ = r"mit"
        most_associated = r"am( meisten)? (assoziiert|verwandt)"
        is_ = r"(ist|sind)"  # for words like "pants"

        base_patterns = [
            rf"Das Wort, das {to_} {category} {most_associated} ist, ist {answer}",
            rf"Das Wort, das {to_} {category} {words} {most_associated} ist, ist {answer}",
            rf"{category} {is_} {most_associated} {to_} {answer}",
            rf"{answer} {is_} {most_associated} {to_} {category}",
            rf"Das Wort {answer} {is_} {most_associated} {to_} {category}",
            rf"Das Wort, das am meisten mit {category} verwandt ist, ist {answer}",
            rf"{answer} ist mit {category} am meisten verwandt",

        ]
        # swap answer and category
        more_base_patterns = [
            swap_substrings(s, subs1=answer, subs2=category) for s in base_patterns
        ]
        base_patterns.extend(more_base_patterns)

        return base_patterns + self.get_shared_patterns(target=answer)

    def get_exact_patterns(self, answer, category):
        return [
            rf"{answer}",
            rf"{category} - {answer}"
        ]

    def negative_scorer(self, prediction, answer):
        score, certainty = None, None

        if not re.search(rf"\b{answer}\b", prediction):
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

        category = metadata["category"]
        distractors = metadata["distractors"]
        answer_index = metadata["answer_index"]
        words = distractors[:answer_index] + [answer] + distractors[answer_index:]

        answer = the_word_regex(answer)
        category = the_word_regex(category)

        exact_patterns = self.get_exact_patterns(answer, category)
        for exact_pattern in exact_patterns:
            score, certainty = self._simple_scorer(prediction, answer=exact_pattern)
            if score:
                return score, certainty

        words = the_words_regex(words)
        of = r"(von)"
        options = r"(Wörtern|Optionen)"
        given = r"(genannten|gegebenen|aufgelisteten|folgenden)"
        words = rf"{of} ({words}|the {given} {options})"

        base_patterns = self.get_base_patterns(answer, category, words)

        self.prefix_kwargs = {"words": words}
        self.suffix_kwargs = {"words": words}

        score, certainty = self.certainty_scorer(prediction, base_patterns)
        return score, certainty
