#for keeping the log while training huge models may be we will require it further when we use LSI or LDA

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)	

# gensim lib the key to everything ...yeah but except BM25

import gensim
from gensim import corpora

# filtering document before training our model. Using pattern , we will convert HTML to plain text

from pattern.web import plaintext
import os 

# output file


documents = []

for fn in os.listdir('.'):
     if os.path.isfile(fn):
        fptr = open(fn,'r+')
        html = fptr.read()
        p_text = plaintext(html, keep={'h1':[], 'h2':[], 'strong':[], 'div':[], 'p':[]})
        p_text = p_text.replace('<',' ').replace('>',' ').replace('/','').replace('h1',' ').replace('h2',' ').replace('strong',' ').replace('div',' ').replace('p',' ').lower()
        documents.append(p_text)
        fptr.close()

stoplist = set('for a of the and to in'.split())
texts = [[word for word in document.lower().split() if word not in stoplist] for document in documents]
dictionary = corpora.Dictionary(texts)
dictionary.filter_extremes(no_below = 1, no_above=0.5, keep_n=50000)
dictionary.save('dictionary.dict')


corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('Corpus.mm', corpus)


tfidf = gensim.models.tfidfmodel.TfidfModel(corpus)
tfidf.save('tf-idfmodel.tfidf_model')

dict_tfidf = {}

for fn in os.listdir('.'):
     if '.html' in fn:
        fptr = open(fn,'r+')
        doc = fptr.read()
        new_vec = dictionary.doc2bow(doc.lower().split())
        tfidf_vec = tfidf[new_vec]
        dict_tfidf[fn] = tfidf_vec
        fptr.close()

target = open('out.tsv', 'a+')

for key, value in dict_tfidf.iteritems():
    target.write(key + '\t')
    target.write(str(value))
    target.write('\n')
target.close()








