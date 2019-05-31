# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 19:25:45 2018

@author: Tamara Amin
"""

import nltk
from nltk.corpus import gutenberg
from nltk.corpus import brown
from nltk.corpus import inaugural
from nltk.corpus import genesis
from nltk import sent_tokenize, word_tokenize, pos_tag, FreqDist, trigrams, bigrams
import re
from collections import Counter
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
import pickle
import csv
import os.path
'''
if os.path.exists('./ngrams_stats_tri.pkl'):# check if file exists:
 #   print "yes"
    #hf = open('ngrams_stats_tri.pkl', 'w')
    with open('ngrams_stats_tri.pkl', 'w') as hf:
        ngrams_stats_tri = pickle.load(hf)
    #hf.close()
  #  ngrams_stats_bi = pickle.load('ngrams_stats_bi.pkl')
  #  ngrams_stats_tri_rev = pickle.load('ngrams_stats_tri_rev.pkl')
  #  ngrams_stats_bi_rev = pickle.load('ngrams_stats_bi_rev.pkl')
else: #initialise
    ngrams_stats_tri={}
    ngrams_stats_bi={}
    ngrams_stats_bi_rev={}
    ngrams_stats_tri_rev={}
'''
#class

ngrams_stats_tri={};
ngrams_stats_bi={}
ngrams_stats_bi_rev={}
ngrams_stats_tri_rev={} 
vocab=Counter()
#choose sample
sample1=brown.raw();
sample2=gutenberg.raw()
sample3=inaugural.raw()
sample5=nltk.corpus.state_union.raw()
sample4=genesis.raw('english-web.txt')
sample=sample1+sample2+sample3+sample4+sample5
vocab,ngrams_stats_tri, ngrams_stats_bi,ngrams_stats_tri_rev, ngrams_stats_bi_rev=mainTrain(vocab,sample,ngrams_stats_tri, ngrams_stats_bi,ngrams_stats_tri_rev, ngrams_stats_bi_rev);

'''
with open('ngrams_stats_tri.pkl', 'w') as hfile:
    pickle.dump(ngrams_stats_tri, hfile)
with open('ngrams_stats_bi.pkl', 'w') as hfile:
    pickle.dump(ngrams_stats_bi, hfile)
with open('ngrams_stats_tri_rev.pkl', 'w') as hfile:
    pickle.dump(ngrams_stats_tri_rev, hfile)
with open('ngrams_stats_bi_rev.pkl', 'w') as hfile:
    pickle.dump(ngrams_stats_bi_rev, hfile)
 
'''
'''
#################### CORPUS USED#############################
gutenberg
brown
 inaugural
 state_union
 genesis.
'''