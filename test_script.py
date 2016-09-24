#for keeping the log while training huge models may be we will require it further when we use LSI or LDA

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)	

# gensim lib the key to everything ...yeah but except BM25

import gensim
from gensim import corpora

# filtering document before training our model. Using pattern , we will convert HTML to plain text

from pattern.web import URL, plaintext
import os 
import math
import sys
# output file

query = sys.argv[1].lower()

dictionary = gensim.corpora.dictionary.Dictionary.load('dictionary.dict')

tfidf = gensim.models.tfidfmodel.TfidfModel.load('tf-idfmodel.tfidf_model')

query_vec = dictionary.doc2bow(query.split())
tfidf_vec = tfidf[query_vec]

tfidf_query_dict = dict(tfidf_vec)


dict_tfidf = {}

with open('out.tsv') as tsv:
    tdidf_doc = [line.strip().split('\t') for line in tsv]

dict_tfidf_doc = {}

i = len(tdidf_doc)
for tup in tdidf_doc:
    if(i):
        dict_tfidf_doc[tdidf_doc[i-1][0]] = tdidf_doc[i-1][1]
        i = i-1

dict_sim_score = {}

for file, tfidf_vec_string in dict_tfidf_doc.iteritems():
    if "), (" in tfidf_vec_string:
        tfidf_vec = tfidf_vec_string.split('), (')
        dict_temp = {}
        for each in tfidf_vec:
            item = each.split(', ')

            dict_temp[int(item[0].replace('(','').replace('[',''))] = float(item[1].replace(')','').replace(']',''))
        norm_query = 0.0000001
        norm_doc = 0.0000001
        sim = 0
        for i in range(0,49999):
            if i in tfidf_query_dict:
                norm_query = norm_query + tfidf_query_dict[i]*tfidf_query_dict[i]
            if i in dict_temp:
                norm_doc = norm_doc + dict_temp[i]*dict_temp[i]
            if i in dict_temp and i in tfidf_query_dict:
                sim = sim + dict_temp[i]*tfidf_query_dict[i]
		norm_query = math.sqrt(norm_query)
		norm_doc = math.sqrt(norm_doc)
		sim = sim/(norm_doc*norm_query)
        dict_sim_score[file] = sim

import collections
sort_dict = collections.Counter(dict_sim_score)
top_10 = sort_dict.most_common(10)
for each in top_10:
    print each
