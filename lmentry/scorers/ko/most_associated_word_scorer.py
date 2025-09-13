import re

from lmentry.scorers.ko.scorer import LMentryScorer, the_word_regex, the_words_regex, swap_substrings


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

        most_associated = r"가장 (연관된|관련된)" 
        more = r"(가장) (많이|더)" 
        is_ = r"(이|가|은|는|와|과|의|에서|을|를)"
        
        base_patterns = [
            rf"{category}{is_} {most_associated} 단어는 {answer}입니다",
            rf"{category}{is_} {words}{is_} {most_associated} 단어는 {answer}입니다",
            rf"{category}{is_} {answer}{is_} {more} 연관되어 있다.",
            rf"{category}{is_} {answer}{is_} {more} 관련되어 있다.",
            rf"{answer}{is_} {category}{is_} {more} 연관된 단어입니다",
            rf"{answer}{is_} {category}{is_} {more} 연관된 단어입니다",
            rf"{category}{is_} {more} 관련된 단어는 {answer}입니다",
            rf"{answer}{is_} 카테고리 {category}{is_} {more} 관련되어 있습니다",
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
        
        options = r"(단어들|옵션들)"
        given = r"(위에|주어진|나열된|다음의)"
        words = rf"({options}|{given} {options} 중에서|{given} {options})"

        base_patterns = self.get_base_patterns(answer, category, words)

        self.prefix_kwargs = {"words": words}
        self.suffix_kwargs = {"words": words}

        score, certainty = self.certainty_scorer(prediction, base_patterns)
        return score, certainty
