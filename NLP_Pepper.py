# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 16:53:38 2018

@author: Tamara Amin
"""

###### TRAIN#####

import nltk
import math
from nltk import sent_tokenize, word_tokenize, pos_tag, FreqDist, trigrams, bigrams, ConditionalFreqDist
import re
from collections import Counter
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
import csv
import unicodedata

#FOR CLEANING SENTENCES 
def cleanSent(sent):
    #process text of sentence: remove punctuation
    sent=re.sub(ur"[^\w\d'\s]+",'',sent);
    sent=sent.lower();
    return sent

#GET DICTIONARY OF TRIGRAM WORDS AND FREQUENCIES
def getTrigramDictionary(fdist_tri,ngrams_statistics_tri):
    for j in range(len(fdist_tri)):
        key=(fdist_tri.items()[j][0][0],fdist_tri.items()[j][0][1]);
        if not ngrams_statistics_tri.has_key(key):
            ngrams_statistics_tri.update({key: Counter()});
            ngrams_statistics_tri[key][(fdist_tri.items()[j][0][2])]=fdist_tri.items()[j][1];
        else:
            ngrams_statistics_tri[key][(fdist_tri.items()[j][0][2])]=fdist_tri.items()[j][1];
    return ngrams_statistics_tri

#GET DICTIONARY OF BIGRAM WORDS AND FREQUENCIES
def getBigramDictionary(fdist_bi,ngrams_statistics_bi):
    for j in range(len(fdist_bi)):
        key=(fdist_bi.items()[j][0][0]);
        if not ngrams_statistics_bi.has_key(key):
            ngrams_statistics_bi.update({key: Counter()});
            ngrams_statistics_bi[key][(fdist_bi.items()[j][0][1])]=fdist_bi.items()[j][1];
        else:
            ngrams_statistics_bi[key][(fdist_bi.items()[j][0][1])]=fdist_bi.items()[j][1];
    return ngrams_statistics_bi

#GET DICTIONARY OF BIGRAM AND TRIGRAM IN FORWARD DIRECTION
    #used for predicting in forward direction (based on words before the blank)
def getNgrams(sent_tokens, ngrams_statistics_tri,ngrams_statistics_bi ):
    sent_len=len(sent_tokens)
    for i in range(sent_len):
        sent=cleanSent(sent_tokens[i]);
    #tokenise sentence
        word_tokens=nltk.word_tokenize(sent);
    #obtan trigrams and bigrams;
        tri_tokens = trigrams(word_tokens);
        bi_tokens = bigrams(word_tokens);
    #obtain frequency distributions;
        fdist_tri = nltk.FreqDist(tri_tokens);
        fdist_bi = nltk.FreqDist(bi_tokens);
    #if there is a trigram,
        ngrams_statistics_tri=getTrigramDictionary(fdist_tri,ngrams_statistics_tri);
     #if there is an bigram   
        ngrams_statistics_bi=getBigramDictionary(fdist_bi,ngrams_statistics_bi);
    return ngrams_statistics_tri, ngrams_statistics_bi;

#REVERSE SENTENCE ORDER
def ReverseSents(sent):
    sent = sent.split();
    sent_rev = " ".join(reversed(sent));
    return sent_rev

#GET DICTIONARY OF BIGRAM AND TRIGRAM IN FORWARD DIRECTION
    #used for predicting in reverse direction (based on words after the blank)
def getReverseNgrams(sent_tokens, ngrams_statistics_tri_rev, ngrams_statistics_bi_rev):
    sent_len=len(sent_tokens);
    
    for i in range(sent_len):
        sent=cleanSent(sent_tokens[i])  ;
    #tokenise sentence
        word_tokens=nltk.word_tokenize(sent);
        word_tokens=list(reversed(word_tokens));
    #obtan trigrams and bigrams
        tri_tokens = trigrams(word_tokens);
        bi_tokens = bigrams(word_tokens);
    #obtain frequency distributions
     #   cond_pairs_tri = (((w0, w1), w2) for w0, w1, w2 in tri_tokens)
       # fdist_tri= ConditionalFreqDist(cond_pairs_tri)
        fdist_tri = nltk.FreqDist(tri_tokens);
        fdist_bi = nltk.FreqDist(bi_tokens);
       # cond_pairs_bi = (((w0), w1) for w0, w1 in bi_tokens)
      #  fdist_bi= ConditionalFreqDist(cond_pairs_bi)
    #get frequency dictionaries
      #if there is a trigram
        ngrams_statistics_tri_rev=getTrigramDictionary(fdist_tri,ngrams_statistics_tri_rev);
        ngrams_statistics_bi_rev=getBigramDictionary(fdist_bi,ngrams_statistics_bi_rev);
    return ngrams_statistics_tri_rev, ngrams_statistics_bi_rev

#GET ALL NGRAMS (bi and tri in both directions)
def getStatistics(vocab,sample,ngrams_statistics_tri, ngrams_statistics_bi,ngrams_statistics_tri_rev, ngrams_statistics_bi_rev ):
    sent_tokens = nltk.sent_tokenize(sample)
    vocab=Counter(nltk.word_tokenize(sample))
    ngrams_statistics_tri, ngrams_statistics_bi=getNgrams(sent_tokens,ngrams_statistics_tri,ngrams_statistics_bi )
    ngrams_statistics_tri_rev, ngrams_statistics_bi_rev=getReverseNgrams(sent_tokens,ngrams_statistics_tri_rev, ngrams_statistics_bi_rev)
    return vocab, ngrams_statistics_tri,ngrams_statistics_bi,ngrams_statistics_tri_rev,ngrams_statistics_bi_rev
'''
def getProbfromFreq(ngrams_stats_fr, vocab):
    alpha=1
    probdict=[[]]
    for key in ngrams_stats_tri:
  '''      
#####WRAPPER FUNCTION THAT TRAINS DICTIONARIES#####
def mainTrain(vocab,sample, ngrams_stats_tri, ngrams_stats_bi,ngrams_stats_tri_rev, ngrams_stats_bi_rev):
    vocab, ngrams_stats_tri, ngrams_stats_bi,ngrams_stats_tri_rev, ngrams_stats_bi_rev=getStatistics(vocab,sample, ngrams_stats_tri, ngrams_stats_bi,ngrams_stats_tri_rev, ngrams_stats_bi_rev)
    #get probabilitievocabs
    
    return vocab,ngrams_stats_tri, ngrams_stats_bi,ngrams_stats_tri_rev, ngrams_stats_bi_rev

'''
#TOKENIZE PHRASE
def getPhraseToke(phrase):
    phrase=phrase.decode('unicode_escape')
    phrase=cleanSent(phrase)
    phrase_tokens=nltk.word_tokenize(phrase)
    return phrase_tokens
#GET VECTOR OF BI/TRI GRAMS BEFORE AND AFTER THE BLANK
def getPhrase(phrase_tokens):
    blank_index=phrase_tokens.index(u"_")
    len_phrase=len(phrase_tokens)
    front_phrase=phrase_tokens[0:blank_index]
    if blank_index==len_phrase-1:
        end_phrase=None
    else:
        end_phrase=phrase_tokens[blank_index+1:len_phrase]
    grams=[None, None, None, None] #[forward tri, forward bi, backward tri, backward bi]
    # find out if there are bigrams, trigrams for both directions
    len_front=len(front_phrase)    
    if len_front>=2:
        grams[0]=(front_phrase[-2],front_phrase[-1])
        grams[1]=(front_phrase[-1])
    elif len_front==1:
        grams[2]=None
        grams[3]=(front_phrase[-1])
    
    if end_phrase == None:
        None
    elif len(end_phrase) >=2:
        grams[2]=(end_phrase[-2], end_phrase[-1])
        grams[3]=(end_phrase[-1])
    else:
        grams[2]=None
        grams[3]=(end_phrase[-1])
    return grams

#GET DICTIONARY OF PREDICTED WORDS
def predict_Gram(phrase_tuple, ngrams_statistics):
    #obtain predicted words for trigrams
    if phrase_tuple in ngrams_statistics.keys():
        predicted=ngrams_statistics[phrase_tuple]

    # remove meaningless stop words
        stop = set(stopwords.words('english'))
        predicted_wstops=predicted.copy()
        for pred in predicted_wstops:
            if pred in stop:
                predicted.pop(pred[0],None)
                predicted=sorted(predicted.iteritems())
                return predicted
    else:
        predicted=None
        return predicted
 
'''
 