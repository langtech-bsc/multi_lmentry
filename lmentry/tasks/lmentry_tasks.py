from __future__ import annotations
import json
import logging
from pathlib import Path

from lmentry.constants import TASKS_DATA_DIR, LANG
from lmentry.tasks.task import LMentryTask

if LANG == "en":
    from lmentry.tasks.en.all_words_from_category import AllWordsFromCategory
    from lmentry.tasks.en.all_words_from_category_0_distractors import AllWordsFromCategory0Distractors
    from lmentry.tasks.en.all_words_from_category_1_distractors import AllWordsFromCategory1Distractors
    from lmentry.tasks.en.all_words_from_category_2_distractors import AllWordsFromCategory2Distractors
    from lmentry.tasks.en.any_words_from_category import AnyWordsFromCategory
    from lmentry.tasks.en.any_words_from_category_3_distractors import AnyWordsFromCategory3Distractors
    from lmentry.tasks.en.any_words_from_category_4_distractors import AnyWordsFromCategory4Distractors
    from lmentry.tasks.en.any_words_from_category_5_distractors import AnyWordsFromCategory5Distractors
    from lmentry.tasks.en.bigger_number import BiggerNumber
    from lmentry.tasks.en.ends_with_letter import EndsWithLetter
    from lmentry.tasks.en.ends_with_word import EndsWithWord
    from lmentry.tasks.en.first_alphabetically import FirstAlphabetically
    from lmentry.tasks.en.first_alphabetically_consecutive_first_letter import FirstAlphabeticallyConsecutiveFirstLetter
    from lmentry.tasks.en.first_alphabetically_different_first_letter import FirstAlphabeticallyDifferentFirstLetter
    from lmentry.tasks.en.first_alphabetically_far_first_letter import FirstAlphabeticallyFarFirstLetter
    from lmentry.tasks.en.first_alphabetically_same_first_letter import FirstAlphabeticallySameFirstLetter
    from lmentry.tasks.en.first_letter import FirstLetter
    from lmentry.tasks.en.first_word import FirstWord
    from lmentry.tasks.en.homophones import Homophones
    from lmentry.tasks.en.last_letter import LastLetter
    from lmentry.tasks.en.last_word import LastWord
    from lmentry.tasks.en.least_associated_word import LeastAssociatedWord
    from lmentry.tasks.en.less_letters import LessLetters
    from lmentry.tasks.en.less_letters_length_diff_3plus import LessLettersLengthDiff3plus
    from lmentry.tasks.en.less_letters_length_diff_1 import LessLettersLengthDiff1
    from lmentry.tasks.en.more_letters import MoreLetters
    from lmentry.tasks.en.more_letters_length_diff_3plus import MoreLettersLengthDiff3plus
    from lmentry.tasks.en.more_letters_length_diff_1 import MoreLettersLengthDiff1
    from lmentry.tasks.en.most_associated_word import MostAssociatedWord
    from lmentry.tasks.en.rhyming_word import RhymingWord
    from lmentry.tasks.en.rhyming_word_orthographically_different import RhymingWordOrthographicallyDifferent
    from lmentry.tasks.en.rhyming_word_orthographically_similar import RhymingWordOrthographicallySimilar
    from lmentry.tasks.en.sentence_containing import SentenceContaining
    from lmentry.tasks.en.sentence_not_containing import SentenceNotContaining
    from lmentry.tasks.en.smaller_number import SmallerNumber
    from lmentry.tasks.en.starts_with_letter import StartsWithLetter
    from lmentry.tasks.en.starts_with_word import StartsWithWord
    from lmentry.tasks.en.word_after import WordAfter
    from lmentry.tasks.en.word_before import WordBefore
    from lmentry.tasks.en.word_containing import WordContaining
    from lmentry.tasks.en.word_not_containing import WordNotContaining

    analysis_tasks = {
    "first_alphabetically_far_first_letter": FirstAlphabeticallyFarFirstLetter,
    "first_alphabetically_different_first_letter": FirstAlphabeticallyDifferentFirstLetter,
    "first_alphabetically_consecutive_first_letter": FirstAlphabeticallyConsecutiveFirstLetter,
    "first_alphabetically_same_first_letter": FirstAlphabeticallySameFirstLetter,
    "any_words_from_category_5_distractors": AnyWordsFromCategory5Distractors,
    "any_words_from_category_4_distractors": AnyWordsFromCategory4Distractors,
    "any_words_from_category_3_distractors": AnyWordsFromCategory3Distractors,
    "all_words_from_category_0_distractors": AllWordsFromCategory0Distractors,
    "all_words_from_category_1_distractors": AllWordsFromCategory1Distractors,
    "all_words_from_category_2_distractors": AllWordsFromCategory2Distractors,
    "rhyming_word_orthographically_similar": RhymingWordOrthographicallySimilar,
    "rhyming_word_orthographically_different": RhymingWordOrthographicallyDifferent,
    "more_letters_length_diff_3plus": MoreLettersLengthDiff3plus,
    "more_letters_length_diff_1": MoreLettersLengthDiff1,
    "less_letters_length_diff_3plus": LessLettersLengthDiff3plus,
    "less_letters_length_diff_1": LessLettersLengthDiff1,
    }

if LANG == "es":
    from lmentry.tasks.es.all_words_from_category import AllWordsFromCategory
    from lmentry.tasks.es.all_words_from_category_0_distractors import AllWordsFromCategory0Distractors
    from lmentry.tasks.es.all_words_from_category_1_distractors import AllWordsFromCategory1Distractors
    from lmentry.tasks.es.all_words_from_category_2_distractors import AllWordsFromCategory2Distractors
    from lmentry.tasks.es.any_words_from_category import AnyWordsFromCategory
    from lmentry.tasks.es.any_words_from_category_3_distractors import AnyWordsFromCategory3Distractors
    from lmentry.tasks.es.any_words_from_category_4_distractors import AnyWordsFromCategory4Distractors
    from lmentry.tasks.es.any_words_from_category_5_distractors import AnyWordsFromCategory5Distractors
    from lmentry.tasks.es.bigger_number import BiggerNumber
    from lmentry.tasks.es.ends_with_letter import EndsWithLetter
    from lmentry.tasks.es.ends_with_word import EndsWithWord
    from lmentry.tasks.es.first_alphabetically import FirstAlphabetically
    from lmentry.tasks.es.first_alphabetically_consecutive_first_letter import FirstAlphabeticallyConsecutiveFirstLetter
    from lmentry.tasks.es.first_alphabetically_different_first_letter import FirstAlphabeticallyDifferentFirstLetter
    from lmentry.tasks.es.first_alphabetically_far_first_letter import FirstAlphabeticallyFarFirstLetter
    from lmentry.tasks.es.first_alphabetically_same_first_letter import FirstAlphabeticallySameFirstLetter
    from lmentry.tasks.es.first_letter import FirstLetter
    from lmentry.tasks.es.first_word import FirstWord
    from lmentry.tasks.es.homophones import Homophones
    from lmentry.tasks.es.last_letter import LastLetter
    from lmentry.tasks.es.last_word import LastWord
    from lmentry.tasks.es.least_associated_word import LeastAssociatedWord
    from lmentry.tasks.es.less_letters import LessLetters
    from lmentry.tasks.es.less_letters_length_diff_3plus import LessLettersLengthDiff3plus
    from lmentry.tasks.es.less_letters_length_diff_1 import LessLettersLengthDiff1
    from lmentry.tasks.es.more_letters import MoreLetters
    from lmentry.tasks.es.more_letters_length_diff_3plus import MoreLettersLengthDiff3plus
    from lmentry.tasks.es.more_letters_length_diff_1 import MoreLettersLengthDiff1
    from lmentry.tasks.es.most_associated_word import MostAssociatedWord
    from lmentry.tasks.es.rhyming_word import RhymingWord
    from lmentry.tasks.es.rhyming_word_orthographically_similar import RhymingWordOrthographicallySimilar
    from lmentry.tasks.es.sentence_containing import SentenceContaining
    from lmentry.tasks.es.sentence_not_containing import SentenceNotContaining
    from lmentry.tasks.es.smaller_number import SmallerNumber
    from lmentry.tasks.es.starts_with_letter import StartsWithLetter
    from lmentry.tasks.es.starts_with_word import StartsWithWord
    from lmentry.tasks.es.word_after import WordAfter
    from lmentry.tasks.es.word_before import WordBefore
    from lmentry.tasks.es.word_containing import WordContaining
    from lmentry.tasks.es.word_not_containing import WordNotContaining

    analysis_tasks = {
    "first_alphabetically_far_first_letter": FirstAlphabeticallyFarFirstLetter,
    "first_alphabetically_different_first_letter": FirstAlphabeticallyDifferentFirstLetter,
    "first_alphabetically_consecutive_first_letter": FirstAlphabeticallyConsecutiveFirstLetter,
    "first_alphabetically_same_first_letter": FirstAlphabeticallySameFirstLetter,
    "any_words_from_category_5_distractors": AnyWordsFromCategory5Distractors,
    "any_words_from_category_4_distractors": AnyWordsFromCategory4Distractors,
    "any_words_from_category_3_distractors": AnyWordsFromCategory3Distractors,
    "all_words_from_category_0_distractors": AllWordsFromCategory0Distractors,
    "all_words_from_category_1_distractors": AllWordsFromCategory1Distractors,
    "all_words_from_category_2_distractors": AllWordsFromCategory2Distractors,
    "rhyming_word_orthographically_similar": RhymingWordOrthographicallySimilar,
    "more_letters_length_diff_3plus": MoreLettersLengthDiff3plus,
    "more_letters_length_diff_1": MoreLettersLengthDiff1,
    "less_letters_length_diff_3plus": LessLettersLengthDiff3plus,
    "less_letters_length_diff_1": LessLettersLengthDiff1,
    }

if LANG == "ca":
    from lmentry.tasks.ca.all_words_from_category import AllWordsFromCategory
    from lmentry.tasks.ca.all_words_from_category_0_distractors import AllWordsFromCategory0Distractors
    from lmentry.tasks.ca.all_words_from_category_1_distractors import AllWordsFromCategory1Distractors
    from lmentry.tasks.ca.all_words_from_category_2_distractors import AllWordsFromCategory2Distractors
    from lmentry.tasks.ca.any_words_from_category import AnyWordsFromCategory
    from lmentry.tasks.ca.any_words_from_category_3_distractors import AnyWordsFromCategory3Distractors
    from lmentry.tasks.ca.any_words_from_category_4_distractors import AnyWordsFromCategory4Distractors
    from lmentry.tasks.ca.any_words_from_category_5_distractors import AnyWordsFromCategory5Distractors
    from lmentry.tasks.ca.bigger_number import BiggerNumber
    from lmentry.tasks.ca.ends_with_letter import EndsWithLetter
    from lmentry.tasks.ca.ends_with_word import EndsWithWord
    from lmentry.tasks.ca.first_alphabetically import FirstAlphabetically
    from lmentry.tasks.ca.first_alphabetically_consecutive_first_letter import FirstAlphabeticallyConsecutiveFirstLetter
    from lmentry.tasks.ca.first_alphabetically_different_first_letter import FirstAlphabeticallyDifferentFirstLetter
    from lmentry.tasks.ca.first_alphabetically_far_first_letter import FirstAlphabeticallyFarFirstLetter
    from lmentry.tasks.ca.first_alphabetically_same_first_letter import FirstAlphabeticallySameFirstLetter
    from lmentry.tasks.ca.first_letter import FirstLetter
    from lmentry.tasks.ca.first_word import FirstWord
    from lmentry.tasks.ca.homophones import Homophones
    from lmentry.tasks.ca.last_letter import LastLetter
    from lmentry.tasks.ca.last_word import LastWord
    from lmentry.tasks.ca.least_associated_word import LeastAssociatedWord
    from lmentry.tasks.ca.less_letters import LessLetters
    from lmentry.tasks.ca.less_letters_length_diff_3plus import LessLettersLengthDiff3plus
    from lmentry.tasks.ca.less_letters_length_diff_1 import LessLettersLengthDiff1
    from lmentry.tasks.ca.more_letters import MoreLetters
    from lmentry.tasks.ca.more_letters_length_diff_3plus import MoreLettersLengthDiff3plus
    from lmentry.tasks.ca.more_letters_length_diff_1 import MoreLettersLengthDiff1
    from lmentry.tasks.ca.most_associated_word import MostAssociatedWord
    from lmentry.tasks.ca.rhyming_word import RhymingWord
    from lmentry.tasks.ca.rhyming_word_orthographically_similar import RhymingWordOrthographicallySimilar
    from lmentry.tasks.ca.sentence_containing import SentenceContaining
    from lmentry.tasks.ca.sentence_not_containing import SentenceNotContaining
    from lmentry.tasks.ca.smaller_number import SmallerNumber
    from lmentry.tasks.ca.starts_with_letter import StartsWithLetter
    from lmentry.tasks.ca.starts_with_word import StartsWithWord
    from lmentry.tasks.ca.word_after import WordAfter
    from lmentry.tasks.ca.word_before import WordBefore
    from lmentry.tasks.ca.word_containing import WordContaining
    from lmentry.tasks.ca.word_not_containing import WordNotContaining

    analysis_tasks = {
    "first_alphabetically_far_first_letter": FirstAlphabeticallyFarFirstLetter,
    "first_alphabetically_different_first_letter": FirstAlphabeticallyDifferentFirstLetter,
    "first_alphabetically_consecutive_first_letter": FirstAlphabeticallyConsecutiveFirstLetter,
    "first_alphabetically_same_first_letter": FirstAlphabeticallySameFirstLetter,
    "any_words_from_category_5_distractors": AnyWordsFromCategory5Distractors,
    "any_words_from_category_4_distractors": AnyWordsFromCategory4Distractors,
    "any_words_from_category_3_distractors": AnyWordsFromCategory3Distractors,
    "all_words_from_category_0_distractors": AllWordsFromCategory0Distractors,
    "all_words_from_category_1_distractors": AllWordsFromCategory1Distractors,
    "all_words_from_category_2_distractors": AllWordsFromCategory2Distractors,
    "rhyming_word_orthographically_similar": RhymingWordOrthographicallySimilar,
    "more_letters_length_diff_3plus": MoreLettersLengthDiff3plus,
    "more_letters_length_diff_1": MoreLettersLengthDiff1,
    "less_letters_length_diff_3plus": LessLettersLengthDiff3plus,
    "less_letters_length_diff_1": LessLettersLengthDiff1,
    }

if LANG == "de":
    from lmentry.tasks.de.all_words_from_category import AllWordsFromCategory
    from lmentry.tasks.de.all_words_from_category_0_distractors import AllWordsFromCategory0Distractors
    from lmentry.tasks.de.all_words_from_category_1_distractors import AllWordsFromCategory1Distractors
    from lmentry.tasks.de.all_words_from_category_2_distractors import AllWordsFromCategory2Distractors
    from lmentry.tasks.de.any_words_from_category import AnyWordsFromCategory
    from lmentry.tasks.de.any_words_from_category_3_distractors import AnyWordsFromCategory3Distractors
    from lmentry.tasks.de.any_words_from_category_4_distractors import AnyWordsFromCategory4Distractors
    from lmentry.tasks.de.any_words_from_category_5_distractors import AnyWordsFromCategory5Distractors
    from lmentry.tasks.de.bigger_number import BiggerNumber
    from lmentry.tasks.de.ends_with_letter import EndsWithLetter
    from lmentry.tasks.de.ends_with_word import EndsWithWord
    from lmentry.tasks.de.first_alphabetically import FirstAlphabetically
    from lmentry.tasks.de.first_alphabetically_consecutive_first_letter import FirstAlphabeticallyConsecutiveFirstLetter
    from lmentry.tasks.de.first_alphabetically_different_first_letter import FirstAlphabeticallyDifferentFirstLetter
    from lmentry.tasks.de.first_alphabetically_far_first_letter import FirstAlphabeticallyFarFirstLetter
    from lmentry.tasks.de.first_alphabetically_same_first_letter import FirstAlphabeticallySameFirstLetter
    from lmentry.tasks.de.first_letter import FirstLetter
    from lmentry.tasks.de.first_word import FirstWord
    from lmentry.tasks.de.homophones import Homophones
    from lmentry.tasks.de.last_letter import LastLetter
    from lmentry.tasks.de.last_word import LastWord
    from lmentry.tasks.de.least_associated_word import LeastAssociatedWord
    from lmentry.tasks.de.less_letters import LessLetters
    from lmentry.tasks.de.less_letters_length_diff_3plus import LessLettersLengthDiff3plus
    from lmentry.tasks.de.less_letters_length_diff_1 import LessLettersLengthDiff1
    from lmentry.tasks.de.more_letters import MoreLetters
    from lmentry.tasks.de.more_letters_length_diff_3plus import MoreLettersLengthDiff3plus
    from lmentry.tasks.de.more_letters_length_diff_1 import MoreLettersLengthDiff1
    from lmentry.tasks.de.most_associated_word import MostAssociatedWord
    from lmentry.tasks.de.rhyming_word import RhymingWord
    from lmentry.tasks.de.rhyming_word_orthographically_similar import RhymingWordOrthographicallySimilar
    from lmentry.tasks.de.sentence_containing import SentenceContaining
    from lmentry.tasks.de.sentence_not_containing import SentenceNotContaining
    from lmentry.tasks.de.smaller_number import SmallerNumber
    from lmentry.tasks.de.starts_with_letter import StartsWithLetter
    from lmentry.tasks.de.starts_with_word import StartsWithWord
    from lmentry.tasks.de.word_after import WordAfter
    from lmentry.tasks.de.word_before import WordBefore
    from lmentry.tasks.de.word_containing import WordContaining
    from lmentry.tasks.de.word_not_containing import WordNotContaining

    analysis_tasks = {
    "first_alphabetically_far_first_letter": FirstAlphabeticallyFarFirstLetter,
    "first_alphabetically_different_first_letter": FirstAlphabeticallyDifferentFirstLetter,
    "first_alphabetically_consecutive_first_letter": FirstAlphabeticallyConsecutiveFirstLetter,
    "first_alphabetically_same_first_letter": FirstAlphabeticallySameFirstLetter,
    "any_words_from_category_5_distractors": AnyWordsFromCategory5Distractors,
    "any_words_from_category_4_distractors": AnyWordsFromCategory4Distractors,
    "any_words_from_category_3_distractors": AnyWordsFromCategory3Distractors,
    "all_words_from_category_0_distractors": AllWordsFromCategory0Distractors,
    "all_words_from_category_1_distractors": AllWordsFromCategory1Distractors,
    "all_words_from_category_2_distractors": AllWordsFromCategory2Distractors,
    "rhyming_word_orthographically_similar": RhymingWordOrthographicallySimilar,
    "more_letters_length_diff_3plus": MoreLettersLengthDiff3plus,
    "more_letters_length_diff_1": MoreLettersLengthDiff1,
    "less_letters_length_diff_3plus": LessLettersLengthDiff3plus,
    "less_letters_length_diff_1": LessLettersLengthDiff1,
    }

if LANG == "pt_br":
    from lmentry.tasks.pt_br.all_words_from_category import AllWordsFromCategory
    from lmentry.tasks.pt_br.all_words_from_category_0_distractors import AllWordsFromCategory0Distractors
    from lmentry.tasks.pt_br.all_words_from_category_1_distractors import AllWordsFromCategory1Distractors
    from lmentry.tasks.pt_br.all_words_from_category_2_distractors import AllWordsFromCategory2Distractors
    from lmentry.tasks.pt_br.any_words_from_category import AnyWordsFromCategory
    from lmentry.tasks.pt_br.any_words_from_category_3_distractors import AnyWordsFromCategory3Distractors
    from lmentry.tasks.pt_br.any_words_from_category_4_distractors import AnyWordsFromCategory4Distractors
    from lmentry.tasks.pt_br.any_words_from_category_5_distractors import AnyWordsFromCategory5Distractors
    from lmentry.tasks.pt_br.bigger_number import BiggerNumber
    from lmentry.tasks.pt_br.ends_with_letter import EndsWithLetter
    from lmentry.tasks.pt_br.ends_with_word import EndsWithWord
    from lmentry.tasks.pt_br.first_alphabetically import FirstAlphabetically
    from lmentry.tasks.pt_br.first_alphabetically_consecutive_first_letter import FirstAlphabeticallyConsecutiveFirstLetter
    from lmentry.tasks.pt_br.first_alphabetically_different_first_letter import FirstAlphabeticallyDifferentFirstLetter
    from lmentry.tasks.pt_br.first_alphabetically_far_first_letter import FirstAlphabeticallyFarFirstLetter
    from lmentry.tasks.pt_br.first_alphabetically_same_first_letter import FirstAlphabeticallySameFirstLetter
    from lmentry.tasks.pt_br.first_letter import FirstLetter
    from lmentry.tasks.pt_br.first_word import FirstWord
    from lmentry.tasks.pt_br.homophones import Homophones
    from lmentry.tasks.pt_br.last_letter import LastLetter
    from lmentry.tasks.pt_br.last_word import LastWord
    from lmentry.tasks.pt_br.least_associated_word import LeastAssociatedWord
    from lmentry.tasks.pt_br.less_letters import LessLetters
    from lmentry.tasks.pt_br.less_letters_length_diff_3plus import LessLettersLengthDiff3plus
    from lmentry.tasks.pt_br.less_letters_length_diff_1 import LessLettersLengthDiff1
    from lmentry.tasks.pt_br.more_letters import MoreLetters
    from lmentry.tasks.pt_br.more_letters_length_diff_3plus import MoreLettersLengthDiff3plus
    from lmentry.tasks.pt_br.more_letters_length_diff_1 import MoreLettersLengthDiff1
    from lmentry.tasks.pt_br.most_associated_word import MostAssociatedWord
    from lmentry.tasks.pt_br.rhyming_word import RhymingWord
    from lmentry.tasks.pt_br.rhyming_word_orthographically_similar import RhymingWordOrthographicallySimilar
    from lmentry.tasks.pt_br.sentence_containing import SentenceContaining
    from lmentry.tasks.pt_br.sentence_not_containing import SentenceNotContaining
    from lmentry.tasks.pt_br.smaller_number import SmallerNumber
    from lmentry.tasks.pt_br.starts_with_letter import StartsWithLetter
    from lmentry.tasks.pt_br.starts_with_word import StartsWithWord
    from lmentry.tasks.pt_br.word_after import WordAfter
    from lmentry.tasks.pt_br.word_before import WordBefore
    from lmentry.tasks.pt_br.word_containing import WordContaining
    from lmentry.tasks.pt_br.word_not_containing import WordNotContaining

    analysis_tasks = {
    "first_alphabetically_far_first_letter": FirstAlphabeticallyFarFirstLetter,
    "first_alphabetically_different_first_letter": FirstAlphabeticallyDifferentFirstLetter,
    "first_alphabetically_consecutive_first_letter": FirstAlphabeticallyConsecutiveFirstLetter,
    "first_alphabetically_same_first_letter": FirstAlphabeticallySameFirstLetter,
    "any_words_from_category_5_distractors": AnyWordsFromCategory5Distractors,
    "any_words_from_category_4_distractors": AnyWordsFromCategory4Distractors,
    "any_words_from_category_3_distractors": AnyWordsFromCategory3Distractors,
    "all_words_from_category_0_distractors": AllWordsFromCategory0Distractors,
    "all_words_from_category_1_distractors": AllWordsFromCategory1Distractors,
    "all_words_from_category_2_distractors": AllWordsFromCategory2Distractors,
    "rhyming_word_orthographically_similar": RhymingWordOrthographicallySimilar,
    "more_letters_length_diff_3plus": MoreLettersLengthDiff3plus,
    "more_letters_length_diff_1": MoreLettersLengthDiff1,
    "less_letters_length_diff_3plus": LessLettersLengthDiff3plus,
    "less_letters_length_diff_1": LessLettersLengthDiff1,
    }

if LANG == "it":
    from lmentry.tasks.it.all_words_from_category import AllWordsFromCategory
    from lmentry.tasks.it.all_words_from_category_0_distractors import AllWordsFromCategory0Distractors
    from lmentry.tasks.it.all_words_from_category_1_distractors import AllWordsFromCategory1Distractors
    from lmentry.tasks.it.all_words_from_category_2_distractors import AllWordsFromCategory2Distractors
    from lmentry.tasks.it.any_words_from_category import AnyWordsFromCategory
    from lmentry.tasks.it.any_words_from_category_3_distractors import AnyWordsFromCategory3Distractors
    from lmentry.tasks.it.any_words_from_category_4_distractors import AnyWordsFromCategory4Distractors
    from lmentry.tasks.it.any_words_from_category_5_distractors import AnyWordsFromCategory5Distractors
    from lmentry.tasks.it.bigger_number import BiggerNumber
    from lmentry.tasks.it.ends_with_letter import EndsWithLetter
    from lmentry.tasks.it.ends_with_word import EndsWithWord
    from lmentry.tasks.it.first_alphabetically import FirstAlphabetically
    from lmentry.tasks.it.first_alphabetically_consecutive_first_letter import FirstAlphabeticallyConsecutiveFirstLetter
    from lmentry.tasks.it.first_alphabetically_different_first_letter import FirstAlphabeticallyDifferentFirstLetter
    from lmentry.tasks.it.first_alphabetically_far_first_letter import FirstAlphabeticallyFarFirstLetter
    from lmentry.tasks.it.first_alphabetically_same_first_letter import FirstAlphabeticallySameFirstLetter
    from lmentry.tasks.it.first_letter import FirstLetter
    from lmentry.tasks.it.first_word import FirstWord
    from lmentry.tasks.it.homophones import Homophones
    from lmentry.tasks.it.last_letter import LastLetter
    from lmentry.tasks.it.last_word import LastWord
    from lmentry.tasks.it.least_associated_word import LeastAssociatedWord
    from lmentry.tasks.it.less_letters import LessLetters
    from lmentry.tasks.it.less_letters_length_diff_3plus import LessLettersLengthDiff3plus
    from lmentry.tasks.it.less_letters_length_diff_1 import LessLettersLengthDiff1
    from lmentry.tasks.it.more_letters import MoreLetters
    from lmentry.tasks.it.more_letters_length_diff_3plus import MoreLettersLengthDiff3plus
    from lmentry.tasks.it.more_letters_length_diff_1 import MoreLettersLengthDiff1
    from lmentry.tasks.it.most_associated_word import MostAssociatedWord
    from lmentry.tasks.it.rhyming_word import RhymingWord
    from lmentry.tasks.it.rhyming_word_orthographically_similar import RhymingWordOrthographicallySimilar
    from lmentry.tasks.it.sentence_containing import SentenceContaining
    from lmentry.tasks.it.sentence_not_containing import SentenceNotContaining
    from lmentry.tasks.it.smaller_number import SmallerNumber
    from lmentry.tasks.it.starts_with_letter import StartsWithLetter
    from lmentry.tasks.it.starts_with_word import StartsWithWord
    from lmentry.tasks.it.word_after import WordAfter
    from lmentry.tasks.it.word_before import WordBefore
    from lmentry.tasks.it.word_containing import WordContaining
    from lmentry.tasks.it.word_not_containing import WordNotContaining

    analysis_tasks = {
    "first_alphabetically_far_first_letter": FirstAlphabeticallyFarFirstLetter,
    "first_alphabetically_different_first_letter": FirstAlphabeticallyDifferentFirstLetter,
    "first_alphabetically_consecutive_first_letter": FirstAlphabeticallyConsecutiveFirstLetter,
    "first_alphabetically_same_first_letter": FirstAlphabeticallySameFirstLetter,
    "any_words_from_category_5_distractors": AnyWordsFromCategory5Distractors,
    "any_words_from_category_4_distractors": AnyWordsFromCategory4Distractors,
    "any_words_from_category_3_distractors": AnyWordsFromCategory3Distractors,
    "all_words_from_category_0_distractors": AllWordsFromCategory0Distractors,
    "all_words_from_category_1_distractors": AllWordsFromCategory1Distractors,
    "all_words_from_category_2_distractors": AllWordsFromCategory2Distractors,
    "rhyming_word_orthographically_similar": RhymingWordOrthographicallySimilar,
    "more_letters_length_diff_3plus": MoreLettersLengthDiff3plus,
    "more_letters_length_diff_1": MoreLettersLengthDiff1,
    "less_letters_length_diff_3plus": LessLettersLengthDiff3plus,
    "less_letters_length_diff_1": LessLettersLengthDiff1,
    }

if LANG == "gl":
    from lmentry.tasks.gl.all_words_from_category import AllWordsFromCategory
    from lmentry.tasks.gl.all_words_from_category_0_distractors import AllWordsFromCategory0Distractors
    from lmentry.tasks.gl.all_words_from_category_1_distractors import AllWordsFromCategory1Distractors
    from lmentry.tasks.gl.all_words_from_category_2_distractors import AllWordsFromCategory2Distractors
    from lmentry.tasks.gl.any_words_from_category import AnyWordsFromCategory
    from lmentry.tasks.gl.any_words_from_category_3_distractors import AnyWordsFromCategory3Distractors
    from lmentry.tasks.gl.any_words_from_category_4_distractors import AnyWordsFromCategory4Distractors
    from lmentry.tasks.gl.any_words_from_category_5_distractors import AnyWordsFromCategory5Distractors
    from lmentry.tasks.gl.bigger_number import BiggerNumber
    from lmentry.tasks.gl.ends_with_letter import EndsWithLetter
    from lmentry.tasks.gl.ends_with_word import EndsWithWord
    from lmentry.tasks.gl.first_alphabetically import FirstAlphabetically
    from lmentry.tasks.gl.first_alphabetically_consecutive_first_letter import FirstAlphabeticallyConsecutiveFirstLetter
    from lmentry.tasks.gl.first_alphabetically_different_first_letter import FirstAlphabeticallyDifferentFirstLetter
    from lmentry.tasks.gl.first_alphabetically_far_first_letter import FirstAlphabeticallyFarFirstLetter
    from lmentry.tasks.gl.first_alphabetically_same_first_letter import FirstAlphabeticallySameFirstLetter
    from lmentry.tasks.gl.first_letter import FirstLetter
    from lmentry.tasks.gl.first_word import FirstWord
    from lmentry.tasks.gl.homophones import Homophones
    from lmentry.tasks.gl.last_letter import LastLetter
    from lmentry.tasks.gl.last_word import LastWord
    from lmentry.tasks.gl.least_associated_word import LeastAssociatedWord
    from lmentry.tasks.gl.less_letters import LessLetters
    from lmentry.tasks.gl.less_letters_length_diff_3plus import LessLettersLengthDiff3plus
    from lmentry.tasks.gl.less_letters_length_diff_1 import LessLettersLengthDiff1
    from lmentry.tasks.gl.more_letters import MoreLetters
    from lmentry.tasks.gl.more_letters_length_diff_3plus import MoreLettersLengthDiff3plus
    from lmentry.tasks.gl.more_letters_length_diff_1 import MoreLettersLengthDiff1
    from lmentry.tasks.gl.most_associated_word import MostAssociatedWord
    from lmentry.tasks.gl.rhyming_word import RhymingWord
    from lmentry.tasks.gl.rhyming_word_orthographically_similar import RhymingWordOrthographicallySimilar
    from lmentry.tasks.gl.sentence_containing import SentenceContaining
    from lmentry.tasks.gl.sentence_not_containing import SentenceNotContaining
    from lmentry.tasks.gl.smaller_number import SmallerNumber
    from lmentry.tasks.gl.starts_with_letter import StartsWithLetter
    from lmentry.tasks.gl.starts_with_word import StartsWithWord
    from lmentry.tasks.gl.word_after import WordAfter
    from lmentry.tasks.gl.word_before import WordBefore
    from lmentry.tasks.gl.word_containing import WordContaining
    from lmentry.tasks.gl.word_not_containing import WordNotContaining

    analysis_tasks = {
    "first_alphabetically_far_first_letter": FirstAlphabeticallyFarFirstLetter,
    "first_alphabetically_different_first_letter": FirstAlphabeticallyDifferentFirstLetter,
    "first_alphabetically_consecutive_first_letter": FirstAlphabeticallyConsecutiveFirstLetter,
    "first_alphabetically_same_first_letter": FirstAlphabeticallySameFirstLetter,
    "any_words_from_category_5_distractors": AnyWordsFromCategory5Distractors,
    "any_words_from_category_4_distractors": AnyWordsFromCategory4Distractors,
    "any_words_from_category_3_distractors": AnyWordsFromCategory3Distractors,
    "all_words_from_category_0_distractors": AllWordsFromCategory0Distractors,
    "all_words_from_category_1_distractors": AllWordsFromCategory1Distractors,
    "all_words_from_category_2_distractors": AllWordsFromCategory2Distractors,
    "rhyming_word_orthographically_similar": RhymingWordOrthographicallySimilar,
    "more_letters_length_diff_3plus": MoreLettersLengthDiff3plus,
    "more_letters_length_diff_1": MoreLettersLengthDiff1,
    "less_letters_length_diff_3plus": LessLettersLengthDiff3plus,
    "less_letters_length_diff_1": LessLettersLengthDiff1,
    }

if LANG == "eu":
    from lmentry.tasks.eu.all_words_from_category import AllWordsFromCategory
    from lmentry.tasks.eu.all_words_from_category_0_distractors import AllWordsFromCategory0Distractors
    from lmentry.tasks.eu.all_words_from_category_1_distractors import AllWordsFromCategory1Distractors
    from lmentry.tasks.eu.all_words_from_category_2_distractors import AllWordsFromCategory2Distractors
    from lmentry.tasks.eu.any_words_from_category import AnyWordsFromCategory
    from lmentry.tasks.eu.any_words_from_category_3_distractors import AnyWordsFromCategory3Distractors
    from lmentry.tasks.eu.any_words_from_category_4_distractors import AnyWordsFromCategory4Distractors
    from lmentry.tasks.eu.any_words_from_category_5_distractors import AnyWordsFromCategory5Distractors
    from lmentry.tasks.eu.bigger_number import BiggerNumber
    from lmentry.tasks.eu.ends_with_letter import EndsWithLetter
    from lmentry.tasks.eu.ends_with_word import EndsWithWord
    from lmentry.tasks.eu.first_alphabetically import FirstAlphabetically
    from lmentry.tasks.eu.first_alphabetically_consecutive_first_letter import FirstAlphabeticallyConsecutiveFirstLetter
    from lmentry.tasks.eu.first_alphabetically_different_first_letter import FirstAlphabeticallyDifferentFirstLetter
    from lmentry.tasks.eu.first_alphabetically_far_first_letter import FirstAlphabeticallyFarFirstLetter
    from lmentry.tasks.eu.first_alphabetically_same_first_letter import FirstAlphabeticallySameFirstLetter
    from lmentry.tasks.eu.first_letter import FirstLetter
    from lmentry.tasks.eu.first_word import FirstWord
    from lmentry.tasks.eu.last_letter import LastLetter
    from lmentry.tasks.eu.last_word import LastWord
    from lmentry.tasks.eu.least_associated_word import LeastAssociatedWord
    from lmentry.tasks.eu.less_letters import LessLetters
    from lmentry.tasks.eu.less_letters_length_diff_3plus import LessLettersLengthDiff3plus
    from lmentry.tasks.eu.less_letters_length_diff_1 import LessLettersLengthDiff1
    from lmentry.tasks.eu.more_letters import MoreLetters
    from lmentry.tasks.eu.more_letters_length_diff_3plus import MoreLettersLengthDiff3plus
    from lmentry.tasks.eu.more_letters_length_diff_1 import MoreLettersLengthDiff1
    from lmentry.tasks.eu.most_associated_word import MostAssociatedWord
    from lmentry.tasks.eu.rhyming_word import RhymingWord
    from lmentry.tasks.eu.rhyming_word_orthographically_similar import RhymingWordOrthographicallySimilar
    from lmentry.tasks.eu.sentence_containing import SentenceContaining
    from lmentry.tasks.eu.sentence_not_containing import SentenceNotContaining
    from lmentry.tasks.eu.smaller_number import SmallerNumber
    from lmentry.tasks.eu.starts_with_letter import StartsWithLetter
    from lmentry.tasks.eu.starts_with_word import StartsWithWord
    from lmentry.tasks.eu.word_after import WordAfter
    from lmentry.tasks.eu.word_before import WordBefore
    from lmentry.tasks.eu.word_containing import WordContaining
    from lmentry.tasks.eu.word_not_containing import WordNotContaining

    analysis_tasks = {
    "first_alphabetically_far_first_letter": FirstAlphabeticallyFarFirstLetter,
    "first_alphabetically_different_first_letter": FirstAlphabeticallyDifferentFirstLetter,
    "first_alphabetically_consecutive_first_letter": FirstAlphabeticallyConsecutiveFirstLetter,
    "first_alphabetically_same_first_letter": FirstAlphabeticallySameFirstLetter,
    "any_words_from_category_5_distractors": AnyWordsFromCategory5Distractors,
    "any_words_from_category_4_distractors": AnyWordsFromCategory4Distractors,
    "any_words_from_category_3_distractors": AnyWordsFromCategory3Distractors,
    "all_words_from_category_0_distractors": AllWordsFromCategory0Distractors,
    "all_words_from_category_1_distractors": AllWordsFromCategory1Distractors,
    "all_words_from_category_2_distractors": AllWordsFromCategory2Distractors,
    "rhyming_word_orthographically_similar": RhymingWordOrthographicallySimilar,
    "more_letters_length_diff_3plus": MoreLettersLengthDiff3plus,
    "more_letters_length_diff_1": MoreLettersLengthDiff1,
    "less_letters_length_diff_3plus": LessLettersLengthDiff3plus,
    "less_letters_length_diff_1": LessLettersLengthDiff1,
    }

if LANG == "ko":
    from lmentry.tasks.ko.all_words_from_category import AllWordsFromCategory
    from lmentry.tasks.ko.all_words_from_category_0_distractors import AllWordsFromCategory0Distractors
    from lmentry.tasks.ko.all_words_from_category_1_distractors import AllWordsFromCategory1Distractors
    from lmentry.tasks.ko.all_words_from_category_2_distractors import AllWordsFromCategory2Distractors
    from lmentry.tasks.ko.any_words_from_category import AnyWordsFromCategory
    from lmentry.tasks.ko.any_words_from_category_3_distractors import AnyWordsFromCategory3Distractors
    from lmentry.tasks.ko.any_words_from_category_4_distractors import AnyWordsFromCategory4Distractors
    from lmentry.tasks.ko.any_words_from_category_5_distractors import AnyWordsFromCategory5Distractors
    from lmentry.tasks.ko.bigger_number import BiggerNumber
    from lmentry.tasks.ko.ends_with_letter import EndsWithLetter
    from lmentry.tasks.ko.ends_with_word import EndsWithWord
    from lmentry.tasks.ko.first_alphabetically import FirstAlphabetically
    # from lmentry.tasks.ko.first_alphabetically_consecutive_first_letter import FirstAlphabeticallyConsecutiveFirstLetter
    # from lmentry.tasks.ko.first_alphabetically_different_first_letter import FirstAlphabeticallyDifferentFirstLetter
    # from lmentry.tasks.ko.first_alphabetically_far_first_letter import FirstAlphabeticallyFarFirstLetter
    # from lmentry.tasks.ko.first_alphabetically_same_first_letter import FirstAlphabeticallySameFirstLetter
    from lmentry.tasks.ko.first_letter import FirstLetter
    from lmentry.tasks.ko.first_word import FirstWord
    from lmentry.tasks.ko.homophones import Homophones
    from lmentry.tasks.ko.last_letter import LastLetter
    from lmentry.tasks.ko.last_word import LastWord
    from lmentry.tasks.ko.least_associated_word import LeastAssociatedWord
    from lmentry.tasks.ko.less_letters import LessLetters
    from lmentry.tasks.ko.less_letters_length_diff_3plus import LessLettersLengthDiff3plus
    from lmentry.tasks.ko.less_letters_length_diff_1 import LessLettersLengthDiff1
    from lmentry.tasks.ko.more_letters import MoreLetters
    from lmentry.tasks.ko.more_letters_length_diff_3plus import MoreLettersLengthDiff3plus
    from lmentry.tasks.ko.more_letters_length_diff_1 import MoreLettersLengthDiff1
    from lmentry.tasks.ko.most_associated_word import MostAssociatedWord
    from lmentry.tasks.ko.rhyming_word import RhymingWord
    from lmentry.tasks.ko.rhyming_word_orthographically_similar import RhymingWordOrthographicallySimilar
    from lmentry.tasks.ko.sentence_containing import SentenceContaining
    from lmentry.tasks.ko.sentence_not_containing import SentenceNotContaining
    from lmentry.tasks.ko.smaller_number import SmallerNumber
    from lmentry.tasks.ko.starts_with_letter import StartsWithLetter
    from lmentry.tasks.ko.starts_with_word import StartsWithWord
    from lmentry.tasks.ko.word_after import WordAfter
    from lmentry.tasks.ko.word_before import WordBefore
    from lmentry.tasks.ko.word_containing import WordContaining
    from lmentry.tasks.ko.word_not_containing import WordNotContaining

    analysis_tasks = {
    # "first_alphabetically_far_first_letter": FirstAlphabeticallyFarFirstLetter,
    # "first_alphabetically_different_first_letter": FirstAlphabeticallyDifferentFirstLetter,
    # "first_alphabetically_consecutive_first_letter": FirstAlphabeticallyConsecutiveFirstLetter,
    # "first_alphabetically_same_first_letter": FirstAlphabeticallySameFirstLetter,
    "any_words_from_category_5_distractors": AnyWordsFromCategory5Distractors,
    "any_words_from_category_4_distractors": AnyWordsFromCategory4Distractors,
    "any_words_from_category_3_distractors": AnyWordsFromCategory3Distractors,
    "all_words_from_category_0_distractors": AllWordsFromCategory0Distractors,
    "all_words_from_category_1_distractors": AllWordsFromCategory1Distractors,
    "all_words_from_category_2_distractors": AllWordsFromCategory2Distractors,
    "rhyming_word_orthographically_similar": RhymingWordOrthographicallySimilar,
    "more_letters_length_diff_3plus": MoreLettersLengthDiff3plus,
    "more_letters_length_diff_1": MoreLettersLengthDiff1,
    "less_letters_length_diff_3plus": LessLettersLengthDiff3plus,
    "less_letters_length_diff_1": LessLettersLengthDiff1,
    }

if LANG == "eu":
    core_tasks = {
    "sentence_containing": SentenceContaining,
    "sentence_not_containing": SentenceNotContaining,
    "word_containing": WordContaining,
    "word_not_containing": WordNotContaining,
    "most_associated_word": MostAssociatedWord,
    "least_associated_word": LeastAssociatedWord,
    "any_words_from_category": AnyWordsFromCategory,
    "all_words_from_category": AllWordsFromCategory,
    "first_alphabetically": FirstAlphabetically,
    "more_letters": MoreLetters,
    "less_letters": LessLetters,
    "bigger_number": BiggerNumber,
    "smaller_number": SmallerNumber,
    "rhyming_word": RhymingWord,
    "word_after": WordAfter,
    "word_before": WordBefore,
    "starts_with_word": StartsWithWord,
    "ends_with_word": EndsWithWord,
    "starts_with_letter": StartsWithLetter,
    "ends_with_letter": EndsWithLetter,
    "first_word": FirstWord,
    "last_word": LastWord,
    "first_letter": FirstLetter,
    "last_letter": LastLetter,
    }
elif LANG == "ko":
    core_tasks = {
    "sentence_containing": SentenceContaining,
    "sentence_not_containing": SentenceNotContaining,
    "word_containing": WordContaining,
    "word_not_containing": WordNotContaining,
    "most_associated_word": MostAssociatedWord,
    "least_associated_word": LeastAssociatedWord,
    "any_words_from_category": AnyWordsFromCategory,
    "all_words_from_category": AllWordsFromCategory,
    "first_alphabetically": FirstAlphabetically,
    "more_letters": MoreLetters,
    "less_letters": LessLetters,
    "bigger_number": BiggerNumber,
    "smaller_number": SmallerNumber,
    "rhyming_word": RhymingWord,
    "homophones": Homophones,
    "word_after": WordAfter,
    "word_before": WordBefore,
    "starts_with_word": StartsWithWord,
    "ends_with_word": EndsWithWord,
    "starts_with_letter": StartsWithLetter,
    "ends_with_letter": EndsWithLetter,
    "first_word": FirstWord,
    "last_word": LastWord,
    "first_letter": FirstLetter,
    "last_letter": LastLetter,
    }
else:
    core_tasks = {
    "sentence_containing": SentenceContaining,
    "sentence_not_containing": SentenceNotContaining,
    "word_containing": WordContaining,
    "word_not_containing": WordNotContaining,
    "most_associated_word": MostAssociatedWord,
    "least_associated_word": LeastAssociatedWord,
    "any_words_from_category": AnyWordsFromCategory,
    "all_words_from_category": AllWordsFromCategory,
    "first_alphabetically": FirstAlphabetically,
    "more_letters": MoreLetters,
    "less_letters": LessLetters,
    "bigger_number": BiggerNumber,
    "smaller_number": SmallerNumber,
    "rhyming_word": RhymingWord,
    "homophones": Homophones,
    "word_after": WordAfter,
    "word_before": WordBefore,
    "starts_with_word": StartsWithWord,
    "ends_with_word": EndsWithWord,
    "starts_with_letter": StartsWithLetter,
    "ends_with_letter": EndsWithLetter,
    "first_word": FirstWord,
    "last_word": LastWord,
    "first_letter": FirstLetter,
    "last_letter": LastLetter,
    }

all_tasks = core_tasks | analysis_tasks


def create_task_data(task_name: str):
    task: LMentryTask = all_tasks[task_name]()
    logging.info(f"creating data for task \"{task_name}\"")
    task.create_data()


def create_all_task_data():
    for task_name in all_tasks:
        create_task_data(task_name)


def count_examples(tasks_to_count: list[str] = None, tasks_data_dir: Path = None):
    tasks_data_dir = tasks_data_dir or TASKS_DATA_DIR

    if tasks_to_count is None:
        tasks_to_count = all_tasks

    n_examples = 0
    for task_name in tasks_to_count:
        task_data_path = tasks_data_dir.joinpath(f"{task_name}.json")
        with open(task_data_path) as f:
            task_data = json.load(f)
            n_examples += len(task_data["examples"])

    print(f"#examples in all tasks combined: {n_examples}")
    return n_examples
