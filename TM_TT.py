# -*- coding: utf-8 -*-
"""
Created on Tue Aug  3 22:58:00 2021

@author: aaron
"""
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
import stanza
import nltk
import nltk.data
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
import numpy as np

# Import the spanish tokenizer
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
spanish_tokenizer = nltk.data.load('tokenizers/punkt/spanish.pickle')
spanish_sw = stopwords.words('spanish')
stanza.download('es')

# Dataset
df = pd.read_csv('C:/Users/VDMG013/Downloads/TRACKING+TELEFONICO_11+enero+2022_16.46/TRACKING TELEFONICO_11 enero 2022_16.46.csv', encoding = 'utf-8')
df = pd.DataFrame({'COMENTS': df.P13A[2:].dropna()})
df = df.reset_index()
df['id'] = df.index
# Split comments and keep ID
word = []
ID = []
identificador = 0
for c in df.COMENTS:
    lw = word_tokenize(c)
    for i in lw:
        word.append(i.lower())
        ID.append(identificador)
    identificador += 1
df_split = pd.DataFrame({
    'id': ID,
    'word': word})
# Remove sw
sw_tt = pd.read_csv('D:/Documents/Tracking_Telefonico/TextMining_TT/sw_tt.csv', encoding = 'latin1')
sw_tt = list(sw_tt['sw'])
sw_tt.append('1.')
sw_tt.append('2.')
sw_tt.append('3.')
sw_tt.append('4.')
sw_tt.append('5.')
sw_tt.append('señal')
sw_tt.append('veces')
sw_tt.append('cobertura')
words_to_drop = [w for w in df_split.word if w in sw_tt]
df_split = df_split[~df_split.word.isin(words_to_drop)]
words_to_drop = [w for w in df_split.word if w in spanish_sw]
df_split = df_split[~df_split.word.isin(words_to_drop)]
# Remake comments without sw
aggregation_functions = {'word':' '.join}
df_clean = df_split.groupby(df_split['id']).aggregate(aggregation_functions)
# Get original comments from df
df_full = df_clean.merge(df, on = 'id')
df_full.to_csv('D:/Documents/Tracking_Telefonico/TextMining_TT/NoRecomendacion/DIC21/NoRecDIC21.csv', encoding = 'latin1', index = False)
# Repeat the process with clean df
text = df_full.word.tolist()
text = ' '.join(map(str, text)) # Single string
text = text.lower()
# Tokenize
text_sw = spanish_tokenizer.tokenize(text) # For sentences
text_sw = word_tokenize(text)
pd.Series(text_sw).value_counts().to_csv('D:/Documents/Tracking_Telefonico/TextMining_TT/NoRecomendacion/DIC21/freq_tokens.csv', encoding = 'latin1')
# Parsing
text_parsed = pd.DataFrame(text_sw)
text_parsed = pd.DataFrame(text_parsed[0].value_counts())
text_parsed = pd.DataFrame({
    'word': text_parsed.index,
    'freq': text_parsed[0]
    })
text_parsed = text_parsed.reset_index(drop=True)
text_parsed['fr_word'] = text_parsed['freq'] / text_parsed.freq.sum()
word = []
docs = []
for w in text_parsed['word']:
    try:
        f = 0
        for c in df_full.word:
            res = re.search('\\b' + str(w) + '\\b', c)
            if type(res) == re.Match:
                f += 1
        docs.append(f)
        word.append(w)
    except:
        docs.append(1)
        word.append(w)
df_docs = pd.DataFrame({
    'word': word,
    'docs': docs})
text_parsed = text_parsed.merge(df_docs, on = 'word')
text_parsed = text_parsed[text_parsed['freq'] > 1]

# POS
pos = stanza.Pipeline(lang = 'es', processors = 'tokenize, mwt, pos')
word = []
upos = []
for w in text_parsed['word']:
    wrd = pos(w)
    for i in wrd.sentences[0].words:
        word.append(i.text)
        upos.append(i.pos)
df_pos = pd.DataFrame({
    'word': word,
    'pos': upos})
text_parsed = text_parsed.merge(df_pos, on = 'word')
# Topic modeling
# Document-Term matrix
vectorizer = TfidfVectorizer(analyzer = 'word',
                             stop_words = sw_tt, min_df = 5, smooth_idf = True)
dtm_tt = vectorizer.fit_transform(df_full['word'])
dtm_tt_dense = dtm_tt.todense()
print("Sparsicity: ", ((dtm_tt_dense == 0).sum() / dtm_tt_dense.size) * 100, "%")
# Topic modeling SVD
svd_model = TruncatedSVD(n_components = 5,
                         algorithm = 'randomized',
                         n_iter = 100,
                         random_state = 100)
svd_model.fit_transform(dtm_tt)
len(svd_model.components_)
topics = vectorizer.get_feature_names()
topic = []
rel_w = []
for i, comp in enumerate(svd_model.components_):
    terms_comp = zip(topics, comp)
    sorted_terms = sorted(terms_comp, key = lambda x:x[1], reverse = True)[:8]
    topic.append('Topic ' + str(i))
    wr = ''
    for t in sorted_terms:
        wr = wr + t[0] + ' '
    rel_w.append(wr[:-1])
topics_tt = pd.DataFrame({
    'topic': topic,
    'words': rel_w
    })
topics_tt.to_csv('D:/Documents/Tracking_Telefonico/TextMining_TT/NoRecomendacion/DIC21/topicos_DIC21.csv', encoding = 'latin1', index = False, errors = 'ignore')
# Comments by topics
topics = svd_model.fit_transform(dtm_tt)
max_topics = np.argmax(topics, axis = 1)
topics_df = pd.DataFrame({'Title': df_full['word'].tolist(),
                           'Topic_Number': max_topics})
topics_df = df_full.merge(topics_df, right_index = True, left_index = True)
topics_df.Topic_Number.value_counts()
df = df = pd.read_csv('C:/Users/VDMG013/Downloads/TRACKING+TELEFONICO_11+enero+2022_16.46/TRACKING TELEFONICO_11 enero 2022_16.46.csv', encoding = 'utf-8', usecols = ['telefono', 'P13A', 'P31_1_TEXT', 'ciudad'])
topics_df = topics_df.merge(df, left_on = 'COMENTS', right_on = 'P13A')
topics_df.to_csv('D:/Documents/Tracking_Telefonico/TextMining_TT/NoRecomendacion/DIC21/text_mining_DIC21.csv', encoding = 'latin1', index = False, errors = 'ignore')
