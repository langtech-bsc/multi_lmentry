# Setting everything up.
import pandas as pd
from pathlib import Path
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize
import string

data_folder = Path('/Users/javierab/Desktop/Work/BSC/lmentry')

# Working on Spanish.
cv_corpus = pd.read_csv(data_folder/'commonvoice_delta15/es/other.tsv', header=0, delimiter='\t', encoding='utf-8')
print('>> There are {} potential sentences in Spanish in the datafile.'.format(len(cv_corpus)))

# Choosing only the suitable sentences (i.e., right lenght and no repeated words).
cv_corpus = cv_corpus[cv_corpus.sentence.notna()]
cv_corpus['num_words'] = cv_corpus['sentence'].apply(word_tokenize).apply(len)
cv_filtered = cv_corpus[(cv_corpus['num_words'] > 5) & (cv_corpus['num_words'] <= 11)]
cv_filtered = cv_filtered.drop_duplicates(['sentence'])
cv_filtered = cv_filtered.drop(columns=['client_id', 'path', 'up_votes', 'down_votes', 'age', 'gender', 'accents', 'variant', 'locale', 'segment', 'num_words'])
print('>> There are {} sentences with the right length in Spanish in the datafile.'.format(len(cv_filtered)))

cv_filtered['sent_no_punct'] = cv_filtered['sentence']
keeps = []
for idex, row in cv_filtered.iterrows():
    row['sent_no_punct'] = word_tokenize(row['sent_no_punct'].translate(str.maketrans('', '', string.punctuation)))
    sent_no_punct = row['sent_no_punct']

    if len(set(sent_no_punct)) == 4:
        keeps.append(0)

    elif len(sent_no_punct) != len(set(sent_no_punct)):
        keeps.append(0)
        
    else:
        keeps.append(1)

cv_filtered['keep'] = keeps
cv_final = cv_filtered[cv_filtered['keep'] == 1].reset_index(drop=True)
cv_final = cv_final.drop(columns=['sent_no_punct', 'keep'])

print('>> There are {} sentences chosen for Spanish in the datafile.'.format(len(cv_final)))

# Saving.
cv_final.to_csv(data_folder/'outputs/es_final_sents_3k.csv', sep='\t')



# Moving on to Catalan.
cv_corpus = pd.read_csv(data_folder/'commonvoice_delta15/ca/other.tsv', header=0, delimiter='\t', encoding='utf-8')
print('>> There are {} potential sentences in Catalan in the datafile.'.format(len(cv_corpus)))

# Choosing only the suitable sentences (i.e., right lenght and no repeated words).
cv_corpus = cv_corpus[cv_corpus.sentence.notna()]
cv_corpus['num_words'] = cv_corpus['sentence'].apply(word_tokenize).apply(len)
cv_filtered = cv_corpus[(cv_corpus['num_words'] > 5) & (cv_corpus['num_words'] <= 11)]
cv_filtered = cv_filtered.drop_duplicates(['sentence'])
cv_filtered = cv_filtered[cv_filtered['variant'].str.contains('Central') == True] # Picking only Central Catalan variant. %%% QUESTION: Do we do the same for Spanish? %%%
cv_filtered = cv_filtered.drop(columns=['client_id', 'path', 'up_votes', 'down_votes', 'age', 'gender', 'accents', 'variant', 'locale', 'segment', 'num_words'])
print('>> There are {} sentences with the right length and variant in Catalan in the datafile.'.format(len(cv_filtered)))

cv_filtered['sent_no_punct'] = cv_filtered['sentence']
keeps = []
for idex, row in cv_filtered.iterrows():
    row['sent_no_punct'] = word_tokenize(row['sent_no_punct'].translate(str.maketrans('', '', string.punctuation)))
    sent_no_punct = row['sent_no_punct']

    if len(set(sent_no_punct)) == 4:
        keeps.append(0)

    elif len(sent_no_punct) != len(set(sent_no_punct)):
        keeps.append(0)
        
    else:
        keeps.append(1)

cv_filtered['keep'] = keeps
cv_final = cv_filtered[cv_filtered['keep'] == 1].reset_index(drop=True)
cv_final = cv_final.drop(columns=['sent_no_punct', 'keep'])

print('>> There are {} sentences chosen for Catalan in the datafile.'.format(len(cv_final)))

# Saving.
cv_final.to_csv(data_folder/'outputs/ca_final_sents_3k.csv', sep='\t')