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

and_present = 0
not_present = 0
and_list = []
not_list = []

if 'and' in query:
    and_present = 1
    temp = query.split('and')
    for i in temp:
        if('not' in i):
            not_present = 1
            temp[temp.index(i)] = i.replace('not','')
            temp_str = i.replace('not','')
            not_list.append(temp[temp.index(temp_str)])
            temp[temp.index(temp_str)] = ''
    and_list = temp

and_list = filter(None, and_list)
not_list = filter(None, not_list)

and_list = [x.strip(' ') for x in and_list]
not_list = [x.strip(' ') for x in not_list]

print and_list
print not_list
print query

dictionary = gensim.corpora.dictionary.Dictionary.load('dictionary.dict')

tfidf = gensim.models.tfidfmodel.TfidfModel.load('tf-idfmodel.tfidf_model')

query_vec = dictionary.doc2bow(query.split())
tfidf_vec = tfidf[query_vec]

tfidf_and_list_dict = {}
tfidf_not_list_dict = {}

if(and_present):
    and_vec = tfidf[dictionary.doc2bow(and_list)]
    tfidf_and_list_dict = dict(and_vec)
    if(not_present):
        not_vec = tfidf[dictionary.doc2bow(not_list)]
        tfidf_not_list_dict = dict(not_vec)

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
        if(and_present):
            if(tfidf_and_list_dict.viewitems() <= dict_temp.viewitems()):
                if(not_present == 0):
                    for i in range(0,49999):
                        if i in tfidf_query_dict:
                            norm_query = norm_query + tfidf_query_dict[i]*tfidf_query_dict[i]
                        if i in dict_temp:
                            norm_doc = norm_doc + dict_temp[i]*dict_temp[i]
                        if i in dict_temp and i in tfidf_query_dict:
                            sim = sim + dict_temp[i]*tfidf_query_dict[i]
                if(not_present):
                    keys_a = set(dict_temp.keys())
                    keys_b = set(tfidf_not_list_dict.keys())
                    intersection = keys_a & keys_b
                    if(len(intersection) == 0):
                        for i in range(0,49999):
                            if i in tfidf_query_dict:
                                norm_query = norm_query + tfidf_query_dict[i]*tfidf_query_dict[i]
                            if i in dict_temp:
                                norm_doc = norm_doc + dict_temp[i]*dict_temp[i]
                            if i in dict_temp and i in tfidf_query_dict:
                                sim = sim + dict_temp[i]*tfidf_query_dict[i]
        if(and_present == 0 and not_present == 0):
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
