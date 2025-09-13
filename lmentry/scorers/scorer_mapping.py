from lmentry.constants import LANG

if LANG == "en":
    from lmentry.scorers.en.all_words_from_category_scorer import AllWordsFromCategoryScorer
    from lmentry.scorers.en.any_words_from_category_scorer import AnyWordsFromCategoryScorer
    from lmentry.scorers.en.bigger_number_scorer import BiggerNumberScorer
    from lmentry.scorers.en.ends_with_letter_scorer import EndsWithLetterScorer
    from lmentry.scorers.en.ends_with_word_scorer import EndsWithWordScorer
    from lmentry.scorers.en.first_alphabetically_scorer import FirstAlphabeticallyScorer
    from lmentry.scorers.en.first_letter_scorer import FirstLetterScorer
    from lmentry.scorers.en.first_word_scorer import FirstWordScorer
    from lmentry.scorers.en.homophone_scorer import HomophoneScorer
    from lmentry.scorers.en.last_letter_scorer import LastLetterScorer
    from lmentry.scorers.en.last_word_scorer import LastWordScorer
    from lmentry.scorers.en.least_associated_word_scorer import LeastAssociatedWordScorer
    from lmentry.scorers.en.less_letters_scorer import LessLettersScorer
    from lmentry.scorers.en.more_letters_scorer import MoreLettersScorer
    from lmentry.scorers.en.most_associated_word_scorer import MostAssociatedWordScorer
    from lmentry.scorers.en.rhyming_word_scorer import RhymingWordScorer
    from lmentry.scorers.en.sentence_containing_scorer import SentenceContainingScorer
    from lmentry.scorers.en.sentence_not_containing_scorer import SentenceNotContainingScorer
    from lmentry.scorers.en.smaller_number_scorer import SmallerNumberScorer
    from lmentry.scorers.en.starts_with_letter_scorer import StartsWithLetterScorer
    from lmentry.scorers.en.starts_with_word_scorer import StartsWithWordScorer
    from lmentry.scorers.en.word_after_scorer import WordAfterScorer
    from lmentry.scorers.en.word_before_scorer import WordBeforeScorer
    from lmentry.scorers.en.word_containing_scorer import WordContainingScorer
    from lmentry.scorers.en.word_not_containing_scorer import WordNotContainingScorer

if LANG == "es":
    from lmentry.scorers.es.all_words_from_category_scorer import AllWordsFromCategoryScorer
    from lmentry.scorers.es.any_words_from_category_scorer import AnyWordsFromCategoryScorer
    from lmentry.scorers.es.bigger_number_scorer import BiggerNumberScorer
    from lmentry.scorers.es.ends_with_letter_scorer import EndsWithLetterScorer
    from lmentry.scorers.es.ends_with_word_scorer import EndsWithWordScorer
    from lmentry.scorers.es.first_alphabetically_scorer import FirstAlphabeticallyScorer
    from lmentry.scorers.es.first_letter_scorer import FirstLetterScorer
    from lmentry.scorers.es.first_word_scorer import FirstWordScorer
    from lmentry.scorers.es.homophone_scorer import HomophoneScorer
    from lmentry.scorers.es.last_letter_scorer import LastLetterScorer
    from lmentry.scorers.es.last_word_scorer import LastWordScorer
    from lmentry.scorers.es.least_associated_word_scorer import LeastAssociatedWordScorer
    from lmentry.scorers.es.less_letters_scorer import LessLettersScorer
    from lmentry.scorers.es.more_letters_scorer import MoreLettersScorer
    from lmentry.scorers.es.most_associated_word_scorer import MostAssociatedWordScorer
    from lmentry.scorers.es.rhyming_word_scorer import RhymingWordScorer
    from lmentry.scorers.es.sentence_containing_scorer import SentenceContainingScorer
    from lmentry.scorers.es.sentence_not_containing_scorer import SentenceNotContainingScorer
    from lmentry.scorers.es.smaller_number_scorer import SmallerNumberScorer
    from lmentry.scorers.es.starts_with_letter_scorer import StartsWithLetterScorer
    from lmentry.scorers.es.starts_with_word_scorer import StartsWithWordScorer
    from lmentry.scorers.es.word_after_scorer import WordAfterScorer
    from lmentry.scorers.es.word_before_scorer import WordBeforeScorer
    from lmentry.scorers.es.word_containing_scorer import WordContainingScorer
    from lmentry.scorers.es.word_not_containing_scorer import WordNotContainingScorer

if LANG == "ca":
    from lmentry.scorers.ca.all_words_from_category_scorer import AllWordsFromCategoryScorer
    from lmentry.scorers.ca.any_words_from_category_scorer import AnyWordsFromCategoryScorer
    from lmentry.scorers.ca.bigger_number_scorer import BiggerNumberScorer
    from lmentry.scorers.ca.ends_with_letter_scorer import EndsWithLetterScorer
    from lmentry.scorers.ca.ends_with_word_scorer import EndsWithWordScorer
    from lmentry.scorers.ca.first_alphabetically_scorer import FirstAlphabeticallyScorer
    from lmentry.scorers.ca.first_letter_scorer import FirstLetterScorer
    from lmentry.scorers.ca.first_word_scorer import FirstWordScorer
    from lmentry.scorers.ca.homophone_scorer import HomophoneScorer
    from lmentry.scorers.ca.last_letter_scorer import LastLetterScorer
    from lmentry.scorers.ca.last_word_scorer import LastWordScorer
    from lmentry.scorers.ca.least_associated_word_scorer import LeastAssociatedWordScorer
    from lmentry.scorers.ca.less_letters_scorer import LessLettersScorer
    from lmentry.scorers.ca.more_letters_scorer import MoreLettersScorer
    from lmentry.scorers.ca.most_associated_word_scorer import MostAssociatedWordScorer
    from lmentry.scorers.ca.rhyming_word_scorer import RhymingWordScorer
    from lmentry.scorers.ca.sentence_containing_scorer import SentenceContainingScorer
    from lmentry.scorers.ca.sentence_not_containing_scorer import SentenceNotContainingScorer
    from lmentry.scorers.ca.smaller_number_scorer import SmallerNumberScorer
    from lmentry.scorers.ca.starts_with_letter_scorer import StartsWithLetterScorer
    from lmentry.scorers.ca.starts_with_word_scorer import StartsWithWordScorer
    from lmentry.scorers.ca.word_after_scorer import WordAfterScorer
    from lmentry.scorers.ca.word_before_scorer import WordBeforeScorer
    from lmentry.scorers.ca.word_containing_scorer import WordContainingScorer
    from lmentry.scorers.ca.word_not_containing_scorer import WordNotContainingScorer

if LANG == "pt_br":
    from lmentry.scorers.pt_br.all_words_from_category_scorer import AllWordsFromCategoryScorer
    from lmentry.scorers.pt_br.any_words_from_category_scorer import AnyWordsFromCategoryScorer
    from lmentry.scorers.pt_br.bigger_number_scorer import BiggerNumberScorer
    from lmentry.scorers.pt_br.ends_with_letter_scorer import EndsWithLetterScorer
    from lmentry.scorers.pt_br.ends_with_word_scorer import EndsWithWordScorer
    from lmentry.scorers.pt_br.first_alphabetically_scorer import FirstAlphabeticallyScorer
    from lmentry.scorers.pt_br.first_letter_scorer import FirstLetterScorer
    from lmentry.scorers.pt_br.first_word_scorer import FirstWordScorer
    from lmentry.scorers.pt_br.homophone_scorer import HomophoneScorer
    from lmentry.scorers.pt_br.last_letter_scorer import LastLetterScorer
    from lmentry.scorers.pt_br.last_word_scorer import LastWordScorer
    from lmentry.scorers.pt_br.least_associated_word_scorer import LeastAssociatedWordScorer
    from lmentry.scorers.pt_br.less_letters_scorer import LessLettersScorer
    from lmentry.scorers.pt_br.more_letters_scorer import MoreLettersScorer
    from lmentry.scorers.pt_br.most_associated_word_scorer import MostAssociatedWordScorer
    from lmentry.scorers.pt_br.rhyming_word_scorer import RhymingWordScorer
    from lmentry.scorers.pt_br.sentence_containing_scorer import SentenceContainingScorer
    from lmentry.scorers.pt_br.sentence_not_containing_scorer import SentenceNotContainingScorer
    from lmentry.scorers.pt_br.smaller_number_scorer import SmallerNumberScorer
    from lmentry.scorers.pt_br.starts_with_letter_scorer import StartsWithLetterScorer
    from lmentry.scorers.pt_br.starts_with_word_scorer import StartsWithWordScorer
    from lmentry.scorers.pt_br.word_after_scorer import WordAfterScorer
    from lmentry.scorers.pt_br.word_before_scorer import WordBeforeScorer
    from lmentry.scorers.pt_br.word_containing_scorer import WordContainingScorer
    from lmentry.scorers.pt_br.word_not_containing_scorer import WordNotContainingScorer

if LANG == "eu":
    from lmentry.scorers.eu.all_words_from_category_scorer import AllWordsFromCategoryScorer
    from lmentry.scorers.eu.any_words_from_category_scorer import AnyWordsFromCategoryScorer
    from lmentry.scorers.eu.bigger_number_scorer import BiggerNumberScorer
    from lmentry.scorers.eu.ends_with_letter_scorer import EndsWithLetterScorer
    from lmentry.scorers.eu.ends_with_word_scorer import EndsWithWordScorer
    from lmentry.scorers.eu.first_alphabetically_scorer import FirstAlphabeticallyScorer
    from lmentry.scorers.eu.first_letter_scorer import FirstLetterScorer
    from lmentry.scorers.eu.first_word_scorer import FirstWordScorer
    from lmentry.scorers.eu.last_letter_scorer import LastLetterScorer
    from lmentry.scorers.eu.last_word_scorer import LastWordScorer
    from lmentry.scorers.eu.least_associated_word_scorer import LeastAssociatedWordScorer
    from lmentry.scorers.eu.less_letters_scorer import LessLettersScorer
    from lmentry.scorers.eu.more_letters_scorer import MoreLettersScorer
    from lmentry.scorers.eu.most_associated_word_scorer import MostAssociatedWordScorer
    from lmentry.scorers.eu.rhyming_word_scorer import RhymingWordScorer
    from lmentry.scorers.eu.sentence_containing_scorer import SentenceContainingScorer
    from lmentry.scorers.eu.sentence_not_containing_scorer import SentenceNotContainingScorer
    from lmentry.scorers.eu.smaller_number_scorer import SmallerNumberScorer
    from lmentry.scorers.eu.starts_with_letter_scorer import StartsWithLetterScorer
    from lmentry.scorers.eu.starts_with_word_scorer import StartsWithWordScorer
    from lmentry.scorers.eu.word_after_scorer import WordAfterScorer
    from lmentry.scorers.eu.word_before_scorer import WordBeforeScorer
    from lmentry.scorers.eu.word_containing_scorer import WordContainingScorer
    from lmentry.scorers.eu.word_not_containing_scorer import WordNotContainingScorer

if LANG == "de":
    from lmentry.scorers.de.all_words_from_category_scorer import AllWordsFromCategoryScorer
    from lmentry.scorers.de.any_words_from_category_scorer import AnyWordsFromCategoryScorer
    from lmentry.scorers.de.bigger_number_scorer import BiggerNumberScorer
    from lmentry.scorers.de.ends_with_letter_scorer import EndsWithLetterScorer
    from lmentry.scorers.de.ends_with_word_scorer import EndsWithWordScorer
    from lmentry.scorers.de.first_alphabetically_scorer import FirstAlphabeticallyScorer
    from lmentry.scorers.de.first_letter_scorer import FirstLetterScorer
    from lmentry.scorers.de.first_word_scorer import FirstWordScorer
    from lmentry.scorers.de.homophone_scorer import HomophoneScorer
    from lmentry.scorers.de.last_letter_scorer import LastLetterScorer
    from lmentry.scorers.de.last_word_scorer import LastWordScorer
    from lmentry.scorers.de.least_associated_word_scorer import LeastAssociatedWordScorer
    from lmentry.scorers.de.less_letters_scorer import LessLettersScorer
    from lmentry.scorers.de.more_letters_scorer import MoreLettersScorer
    from lmentry.scorers.de.most_associated_word_scorer import MostAssociatedWordScorer
    from lmentry.scorers.de.rhyming_word_scorer import RhymingWordScorer
    from lmentry.scorers.de.sentence_containing_scorer import SentenceContainingScorer
    from lmentry.scorers.de.sentence_not_containing_scorer import SentenceNotContainingScorer
    from lmentry.scorers.de.smaller_number_scorer import SmallerNumberScorer
    from lmentry.scorers.de.starts_with_letter_scorer import StartsWithLetterScorer
    from lmentry.scorers.de.starts_with_word_scorer import StartsWithWordScorer
    from lmentry.scorers.de.word_after_scorer import WordAfterScorer
    from lmentry.scorers.de.word_before_scorer import WordBeforeScorer
    from lmentry.scorers.de.word_containing_scorer import WordContainingScorer
    from lmentry.scorers.de.word_not_containing_scorer import WordNotContainingScorer

task_name_to_scorer = {
    "starts_with_word": StartsWithWordScorer,
    "ends_with_word": EndsWithWordScorer,
    "starts_with_letter": StartsWithLetterScorer,
    "ends_with_letter": EndsWithLetterScorer,
    "most_associated_word": MostAssociatedWordScorer,
    "least_associated_word": LeastAssociatedWordScorer,
    "any_words_from_category": AnyWordsFromCategoryScorer,
    "all_words_from_category": AllWordsFromCategoryScorer,
    "sentence_containing": SentenceContainingScorer,
    "sentence_not_containing": SentenceNotContainingScorer,
    "word_containing": WordContainingScorer,
    "word_not_containing": WordNotContainingScorer,
    "rhyming_word": RhymingWordScorer,
    "homophones": HomophoneScorer,
    "first_word": FirstWordScorer,
    "last_word": LastWordScorer,
    "first_letter": FirstLetterScorer,
    "last_letter": LastLetterScorer,
    "word_after": WordAfterScorer,
    "word_before": WordBeforeScorer,
    "more_letters": MoreLettersScorer,
    "less_letters": LessLettersScorer,
    "first_alphabetically": FirstAlphabeticallyScorer,
    "bigger_number": BiggerNumberScorer,
    "smaller_number": SmallerNumberScorer
}
