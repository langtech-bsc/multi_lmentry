"""
Creates the necessary files for any LMEntry language.
We do not need to convert plurals.json and phonetically_unambiguous_words.json; We do that in the same script
BEFORE USE: Check input file paths in LANG_CSV_MAP
USE: python3 conversor.py --lang "es" --mode "verbs" --output_path "/gpfs/projects/bsc88/projects/lmentry/resources/de/"
"""

import warnings
warnings.filterwarnings("ignore")

import csv
import json
import os
import sys
import random
import argparse
import pandas as pd
import re
import urllib.request
from tqdm import tqdm
import codecs

# WordNet
import nltk

# nltk.download('omw')
# Available langs in NLTK WordNet: https://omwn.org/omw1.html
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
# German WordNet
# from germanetpy import germanet
# Multilingual dictionary for synonyms
# from PyMultiDictionary import MultiDictionary, DICT_EDUCALINGO
# Phonetic transcription
# import epitran
# Spanish and Catalan rhyme extractor
# from pyverse import Pyverse
# Language-agnostic rhyme extractor
from nltk import SyllableTokenizer

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
print(sys.path[0])

# Define a dictionary to map languages to CSV file paths
LANG_CSV_MAP = {
    "es": {
        "default": "es_vocabulario_elemental_pos_phon.csv",
        "homophones": "es_pal_written_query.csv",
        "encoding": "utf-8"
    },
    "ca": {
        "default": "ca_vocabulari_elemental_pos_phon.csv",
        "homophones": "ca_vocabulari_elemental_pos_phon.csv",
        "encoding": "utf-8"
    },
    "pt_br": {
        "default": "pt_br_vocabulario_elementar_pos_phon.csv",
        "homophones": "pt_br_homophones.csv",
        "encoding": "utf-8"
    },
    "de": {
        "default": "de_Grundwortschatz_pos_phon.csv",
        "homophones": "de_Grundwortschatz_pos_phon.csv",
        "encoding": "utf-8-sig"
    },
    "ko": {
        "default": "ko_vocabulario_elemental_pos_phon.csv",
        "homophones": "ko_homophones.csv",
        "encoding": "utf-8"
    },
    "eu": {
        "default": "eu_oinarrizko_hiztegia_pos_phon.csv",
        "homophones": "eu_oinarrizko_hiztegia_pos_phon.csv",
        "encoding": "utf-8"
    },
    "it": {
        "default": "it_elemental_vocabulary_pos_phon.tsv",
        "homophones": "it_homophones.tsv",
        "encoding": "utf-8"
    },
    "gl": {
        "default": "gl_vocabulario_elemental_pos_phon.csv",
        "homophones": "gl_homophones.csv",
        "encoding": "utf-8"
    },
}


def transliterate(args, word):

    map2epilang = {
        "de": "deu-Latn",
        "es": "spa-Latn-eu",  # Spanish (Spain)
        "en": "eng-Latn",
        "ca": "cat-Latn",  # Limited support
        "eu": "",  # No support
        "gl": "",  # No support
        "pt_br": "por-Latn",  # Limited support
        #"ko": "",  # No support, they already provided homophones
        "it": "ita-Latn",
    }

    # Initialize Epitran transliterator
    epi = epitran.Epitran(map2epilang[args.lang])

    return epi.transliterate(word)


def format_words_json(reader):
    formatted_words = {}

    for row_num, row in enumerate(reader, start=1):
        try:
            formatted_words[row["word"]] = {
                "pos": row["pos"],
            }
        except UnicodeDecodeError as e:
            print(f"Error decoding row {row_num}: {e}")
            continue

    return formatted_words


def get_rhyme(word, transcription, args):
    # Function to extract consonant rhymes from transcriptions
    if args.lang in ["es", "ca", "it", "gl", "pt"]:
        syl = Pyverse(word)
        rhyme = syl.consonant_rhyme
        try:
            trans_rhyme = transcription[-len(rhyme):]
        except:
            # Some transcriptions are shorter than the actual word
            # e.g. aguila > aGila / ocho > oCo
            trans_rhyme = transcription[-(len(rhyme) - 1):]
    else:
        # Since we cannot guess the last tonic syllable based on the transcription
        # we take the last syllable for the rest of the languages
        syl_tokenizer = SyllableTokenizer()
        trans_rhyme = syl_tokenizer.tokenize(transcription)[-1]

    return trans_rhyme


def format_rhyme_json(reader, args):
    formatted_rhyme = {}

    for row in reader:
        try:
            rhyme = get_rhyme(row["word"].strip(), row["transcription"], args=args)
        except ValueError as e:
            print("Failed finding rhyme for {} as {}".format(row, e))
            continue

        if rhyme not in formatted_rhyme:
            formatted_rhyme[rhyme] = list()

        formatted_rhyme[rhyme].append(row["word"].strip())

    print(f"{len(formatted_rhyme.keys())} different rhymes.")

    # Remove key-value pairs that have 1 value
    for key in formatted_rhyme.copy().keys():
        if len(formatted_rhyme[key]) <= 1:
            formatted_rhyme.pop(key)

    print(f"{len(formatted_rhyme.keys())} different rhymes after removing single groups.")

    return formatted_rhyme


def format_homophones(reader, args):
    # Catalan, Spanish homophones are extracted manually
    formatted_homophones = {}

    if args.lang == "es":
        # Spanish homophones were originally extracted automatically from the es_pal wordlist
        # The script output too many of them, so we instead extracted a list manually
        # Manual list is in resources/es/homophones.csv
        for row in reader:
            if len(row["word"]) <= 2 or row["word"].isascii() == False:
                continue

            trans = row["es_phon_structure"]

            if trans not in formatted_homophones:
                formatted_homophones[trans] = list()

            formatted_homophones[trans].append(row["word"])
    if args.lang == "it":
        # Italian homophones were already given
        for row in reader:
            print(row)
            trans = transliterate(args, row["word"])

            if trans not in formatted_homophones:
                formatted_homophones[trans] = list()

            formatted_homophones[trans].append(row["word"])
            formatted_homophones[trans].append(row["homophones"])

    else:
        for row in reader:
            trans = row["transcription"]

            if trans not in formatted_homophones:
                formatted_homophones[trans] = list()

            formatted_homophones[trans].append(row["word"])

    for key in formatted_homophones.copy().keys():
        # Remove key-value pairs that have 1 value
        if len(formatted_homophones[key]) <= 1:
            formatted_homophones.pop(key)
        # Remove key-value pairs where values are the same
        elif len(formatted_homophones[key]) >= 2 and all(
                word.lower() == formatted_homophones[key][0].lower() for word in formatted_homophones[key]):
            formatted_homophones.pop(key)
    for key in formatted_homophones:
        print(f"[INFO] Key {key} has {formatted_homophones[key]} homophones.")

    return formatted_homophones


def format_words(lexicon):
    print("[INFO] There are {} words distributed across {} categories in the initial lexicon.".format(
        len(lexicon),
        lexicon['category'].nunique(),
    ))

    # Creating a dictionary of the nouns included in each category.
    lexicon = lexicon.drop(columns=['pos', 'transcription'])
    lex_in_cats = lexicon.groupby('category')['word'].apply(list)
    lex_dict = lex_in_cats.to_dict()

    return lex_dict


def format_verbs(lexicon):
    print("[INFO] There are {} words distributed across {} categories in the initial lexicon.".format(
        len(lexicon),
        lexicon['category'].nunique(),
    ))
    verbs = lexicon[lexicon['pos'].str.match('VERB') == True]
    print("[INFO] There are {} verbs distributed across {} categories in the lexicon.".format(
        len(verbs),
        verbs['category'].nunique(),
    ))

    # Creating a dictionary of the nouns included in each category.
    verbs = verbs.drop(columns=['pos', 'transcription'])
    verbs_in_cats = verbs.groupby('category')['word'].apply(list)
    verbs_dict = verbs_in_cats.to_dict()

    return verbs_dict


def format_nouns(lexicon):
    print('[INFO] There are {} words distributed across {} categories in the initial lexicon.'.format(
        len(lexicon),
        lexicon['category'].nunique()
    ))
    nouns = lexicon[lexicon['pos'].str.contains('NOUN') == True]
    print('[INFO] There are {} nouns distributed across {} categories in the lexicon.'.format(
        len(nouns),
        nouns['category'].nunique()
    ))

    # Creating a dictionary of the nouns included in each category.
    nouns = nouns.drop(columns=['pos', 'transcription'])
    nouns_in_cats = nouns.groupby('category')['word'].apply(list)
    noun_dict = nouns_in_cats.to_dict()

    return noun_dict


def read_csv_and_format(csv_filepath, args):
    print("args:", args)
    if "es_pal" in csv_filepath or args.lang == "it":
        delim = "\t"
    else:
        delim = ","

    # These are processed with pandas
    if args.mode == "verbs":
        lexicon = pd.read_csv(csv_filepath, header=0, delimiter=delim, encoding=LANG_CSV_MAP[args.lang]["encoding"])
        formatted_data = format_verbs(lexicon)
    if args.mode == "nouns":
        lexicon = pd.read_csv(csv_filepath, header=0, delimiter=delim, encoding=LANG_CSV_MAP[args.lang]["encoding"])
        formatted_data = format_nouns(lexicon)
    if args.mode == "words_category":
        lexicon = pd.read_csv(csv_filepath, header=0, delimiter=delim, encoding=LANG_CSV_MAP[args.lang]["encoding"])
        formatted_data = format_words(lexicon)

    # These are processed iteratively with CSV reader
    else:
        with codecs.open(csv_filepath, 'rb', encoding=LANG_CSV_MAP[args.lang]["encoding"]) as csv_file:
            reader = csv.DictReader(csv_file, delimiter=delim)

            if args.mode == "words":
                formatted_data = format_words_json(reader)
            if args.mode == "rhyme":
                formatted_data = format_rhyme_json(reader, args)
            if args.mode == "homophones":
                formatted_data = format_homophones(reader, args)

    if args.mode == "homophones":
        csv_filepath = os.path.join(sys.path[0], "converters", "data", LANG_CSV_MAP[args.lang]["default"])
        raw_data = pd.read_csv(csv_filepath, header=0, delimiter=delim, encoding=LANG_CSV_MAP[args.lang]["encoding"])
    else:
        raw_data = pd.read_csv(csv_filepath, header=0, delimiter=delim, encoding=LANG_CSV_MAP[args.lang]["encoding"])

    return formatted_data, raw_data


def save_as_json(formatted_data, output_dirpath, mode, indent):
    if mode == "words":
        json_filepath = os.path.join(output_dirpath, f'lmentry_words.json')
    if mode == "rhyme":
        json_filepath = os.path.join(output_dirpath, f'rhyme_groups.json')
    if mode == "verbs":
        json_filepath = os.path.join(output_dirpath, f'verbs_by_category.json')
    if mode == "nouns":
        json_filepath = os.path.join(output_dirpath, f'nouns_by_category.json')
    if mode == "words_category":
        json_filepath = os.path.join(output_dirpath, f'words_by_category.json')
    if mode == "homophones":
        raise ValueError("Homophones mode generates a CSV file not a JSON file.")

    print("[INFO] Saving to {}".format(json_filepath))
    with open(json_filepath, 'w', encoding="utf-8") as json_file:
        json.dump(formatted_data, json_file, indent=indent, ensure_ascii=False)
    print("[INFO] Saved to {}".format(json_filepath))


class HomophonesCSVGenerator:
    def __init__(self, formatted_data, unformatted_data, args):
        self.formatted_data = formatted_data
        self.unformatted_data = unformatted_data
        self.args = args
        self.dictionary = MultiDictionary()
        if self.args.lang == "de":
            try:
                self.path_germanet_XML_files_gpfs = os.path.join(sys.path[0], "converters", "data", "germanet_data",
                                                                 "GN_V180", "GN_V180_XML")
                self.path_germanet_XML_files_local = "/home/jsainz/Downloads/lmentry_data/GN_V180/GN_V180/GN_V180_XML"
                self.germanet = germanet.Germanet(self.path_germanet_XML_files_local)
                print("[INFO] Searching synonyms with GermaNet")
            except:
                self.germanet = None
                print("[INFO] Searching synonyms with MultiDictionary")

    def get_random_word(self):
        random_word = random.choice(list(self.unformatted_data["word"]))
        return random_word

    def find_synonym(self, word):
        synonyms = set()
        map2nltklang = {
            "es": "spa",
            "en": "eng",
            "ca": "cat",
            "eu": "eus",
            "gl": "glg",
            "pt_br": "por",
            #"it": "it",
        }

        if self.args.lang in map2nltklang:
            synsets = wn.synsets(word, lang=map2nltklang[self.args.lang])

            for synset in synsets:
                lemmas = synset.lemmas(self.args.lang)
                synonyms.update(lemma.name() for lemma in lemmas
                                if lemma.name() != word
                                and "_" not in lemma.name())
        if self.args.lang in ["de"]:
            if not self.germanet:
                # If germanetpy does not find the data at /lmentry/resources/converters/data/germanet_data
                # it will use PyMultiDictionary but it will not find all synonyms
                synonyms = [word for word in self.dictionary.synonym(lang='de', word=word) if
                            not re.search(r'\s', word)]
            else:
                synsets = self.germanet.get_synsets_by_orthform(word)

                for synset in synsets:
                    lemmas = synset.lexunits
                    synonyms.update(lemma.orthform for lemma in lemmas
                                    if lemma.orthform != word
                                    and "_" not in lemma.orthform
                                    and not re.search(r'\s', lemma.orthform))

        if len(list(synonyms)) > 1 or not all(element == "" for element in synonyms):
            return list(synonyms)
        else:
            return ""

    def get_related_words(self, word):
        # Lemmatize the word to find its root form
        lemmatizer = WordNetLemmatizer()
        lemma = lemmatizer.lemmatize(word)
        return self.find_synonym(lemma)

    def get_synonyms(self, word1, word2):

        synonyms = self.find_synonym(word1)

        if synonyms == "":
            related = self.get_related_words(word1)
            return related

        return synonyms

    def search_other_homophones(self):

        if self.args.lang == "de":
            german_wordlist_url = "https://gist.githubusercontent.com/MarvinJWendt/2f4f4154b8ae218600eb091a5706b5f4/raw/36b70dd6be330aa61cd4d4cdfda6234dcb0b8784/wordlist-german.txt"
            f = urllib.request.urlopen(german_wordlist_url)
            all_wordlist = [str(word).replace("\\n", "").replace("b'", "").replace("'", "") for word in f.readlines() if
                            len(str(word)) >= 2]
            random_wordlist = random.sample(all_wordlist, 300000)

        curated_wordlist = list(self.unformatted_data["word"])
        formatted_homophones = {}

        # Find homophones
        for word in tqdm(random_wordlist, desc="Processing words"):
            transliteration = transliterate(self.args, word)
            if transliteration not in formatted_homophones:
                formatted_homophones[transliteration] = []
            if word not in formatted_homophones[transliteration]:
                formatted_homophones[transliteration].append(word)

        for key, values in formatted_homophones.copy().items():
            # Remove key-value pairs that have 1 value
            if len(values) <= 1:
                formatted_homophones.pop(key)
            # Remove key-value pairs where values are the same
            elif len(values) >= 2 and all(word.lower() == values[0].lower() for word in values):
                formatted_homophones.pop(key)
        for key in formatted_homophones:
            print(f"[INFO] Key {key} has {formatted_homophones[key]} homophones.")

        return formatted_homophones

    def save_as_homophones_csv(self, output_dirpath):
        csv_outpath = os.path.join(output_dirpath, 'homophones.csv')

        df = pd.DataFrame(columns=["change", "word", "homophone", "semantic1", "semantic2", "easy1", "easy2"])

        #extra_homophones = self.search_other_homophones()
        #self.formatted_data.update(extra_homophones)
        print("[{} homophones".format(len(self.formatted_data)))

        for k, v in tqdm(self.formatted_data.items(), desc="Processing words"):
            synonyms = self.get_synonyms(v[0], v[1])
            if synonyms != "":
                if len(synonyms) >= 2:
                    print(synonyms)
                    new_line = pd.DataFrame({"change": [k],
                                             "word": [v[0]],
                                             "homophone": [v[1]],
                                             "semantic1": [self.get_random_word()],
                                             "semantic2": [self.get_random_word()],
                                             "easy1": [self.get_random_word()],
                                             "easy2": [self.get_random_word()]})

                    df = pd.concat([df, new_line], ignore_index=True)
            else:
                print("[ERROR] Could not find synonyms for word {}.".format(v))
                new_line = pd.DataFrame({"change": [k],
                                         "word": [v[0]],
                                         "homophone": [v[1]],
                                         "semantic1": [self.get_random_word()],
                                         "semantic2": [self.get_random_word()],
                                         "easy1": [self.get_random_word()],
                                         "easy2": [self.get_random_word()]})

                df = pd.concat([df, new_line], ignore_index=True)

        with open(csv_outpath, "w") as out_file:
            df.to_csv(out_file, index=False)
        print("[INFO] Data saved to {}".format(csv_outpath))


def main():
    parser = argparse.ArgumentParser(description="Process CSV files and save formatted data as JSON.")

    parser.add_argument("--lang",
                        type=str,
                        choices=["es", "ca", "eu", "gl", "pt_br", "de", "ko", "it"],
                        help="Language to process.",
                        required=True, )
    parser.add_argument("--mode",
                        type=str,
                        choices=["words", "rhyme", "homophones", "verbs", "nouns", "words_category"],
                        help="'words' creates lmentry_words.json\n"
                             "'rhyme' creates rhyme_groups.json\n"
                             "'homophones' creates homophones.csv\n"
                             "'verbs' creates verbs_by_category.json\n"
                             "'nouns' creates nouns_by_category.json\n"
                             "'words_category' creates words_by_category.json\n",
                        required=True, )
    parser.add_argument("--output_path",
                        type=str,
                        help="Output path",
                        required=False)

    args = parser.parse_args()

    if not args.output_path:
        args.output_path = os.path.join(sys.path[0], args.lang)

    if args.lang == "de" and args.mode == "homophones":
        print("\n[WARNING] German homophones uses pygermanet library (not NLTK)."
              "\nData is in /lmentry/resources/converters/data/germanet_data"
              "\nOtherwise the script will use PyMultiDictionary but works bad.\n")

    if args.lang in ["ko", "ca", "es"] and args.mode == "homophones":
        print("\n[ERROR] Homophones list was already gathered manually/ provided.")

    # Get input file path from selected language & mode
    if args.mode == "homophones":
        # The homophones mode generates a CSV file from another elemental vocabulary CSV file + Wordnet
        # e.g. /lmentry/resources/converters/data/de_Grundwortschatz_pos_phon.csv
        csv_filepath = os.path.join(sys.path[0], "converters", "data", LANG_CSV_MAP[args.lang]["homophones"])
        print("[INFO] Reading {}".format(csv_filepath))
        formatted_data, raw_data = read_csv_and_format(csv_filepath, args=args)
        generator = HomophonesCSVGenerator(formatted_data, raw_data, args)
        generator.save_as_homophones_csv(args.output_path)
    else:
        # The rest of the modes generate a JSON file from the elemental vocabulary CSV file
        csv_filepath = os.path.join(sys.path[0], "converters", "data", LANG_CSV_MAP[args.lang]["default"])
        print("[INFO] Reading {}".format(csv_filepath))
        formatted_data, _ = read_csv_and_format(csv_filepath, args=args)
        save_as_json(formatted_data, output_dirpath=args.output_path, mode=args.mode, indent=2)

    if not csv_filepath:
        raise ValueError("CSV file path not available for the selected language.")


if __name__ == "__main__":
    print("[INFO] Default encoding {}".format(sys.getdefaultencoding()))
    random.seed(1)
    main()
