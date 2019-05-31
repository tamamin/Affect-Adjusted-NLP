# -*- coding: utf-8 -*-
"""
Created on Tue May 01 21:57:05 2018

@author: Tamara Amin
"""

#P####REDICTION#######################


import nltk
import math
from collections import Counter
from nltk.corpus import stopwords
import csv


#FOR CLEANING SENTENCES 
def cleanSent(sent):
    #process text of sentence: remove punctuation
    sent=re.sub(ur"[^\w\d'\s]+",'',sent);
    sent=sent.lower();
    return sent

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
def predict_Gram(vocab, phrase_tuple, ngrams_statistics):
    #obtain predicted words for trigrams
    predicted_norm={}
    v_len=float(len(vocab))
    if phrase_tuple in ngrams_statistics.keys():
        predicted=ngrams_statistics[phrase_tuple]
        total=sum(predicted.values())
        predicted_norm = dict(predicted)
        predicted_norm.update((k, ((float(v)+ 1.0)/(float(total)+ v_len)))for k,v in predicted_norm.items())
  #      print("pnorm type")
  #      print(type(predicted_norm))
    
    # remove meaningless stop words
        stop = set(stopwords.words('english'))
        predicted_wstops=predicted_norm.copy()
        for pred in predicted_wstops:
            if pred in stop:
                predicted_norm.pop(pred[0],None)
                return predicted_norm
    else:
        predicted=None
  #  print "predict Gram"
  #  print type(predicted_norm)
    #print predicted_norm
    return predicted_norm
 
def predict(vocab, phrase_gram, ngrams_stats_tri, ngrams_stats_bi,ngrams_stats_tri_rev, ngrams_stats_bi_rev):
    #[forward tri, forward bi, backward tri, backward bi]
    
  #  print 1
    predicted_tri =None
    predicted_bi =None
    predicted_bi_rev =None
    predicted_tri_rev =None
    
  #  print 2
    if phrase_gram[0] is not None:
        predicted_tri=predict_Gram(vocab, phrase_gram[0],ngrams_stats_tri)
            
     #   print "predict 0"
    #    print type(predicted_tri)
    predicted_bi= predict_Gram(vocab, phrase_gram[1],ngrams_stats_bi)
    if phrase_gram[2] is not None:
      #  print 3
        predicted_tri_rev=predict_Gram(vocab, phrase_gram[2],ngrams_stats_tri_rev)
        
    if phrase_gram[3] is not None:
     #   print 4
        predicted_bi_rev= predict_Gram(vocab, phrase_gram[3],ngrams_stats_bi_rev)
    
   # print "predict 1"
  #  print type(predicted_tri) 
    return predicted_tri, predicted_bi, predicted_tri_rev, predicted_bi_rev

def mergePredictions(pred_tri, pred_bi, pred_tri_rev, pred_bi_rev):
    #pred_merged={}
    
    pred_tri = pred_tri if pred_tri else {}
    pred_bi = pred_bi if pred_bi else {}
    pred_tri_rev = pred_tri_rev if pred_tri_rev else {}
    pred_bi_rev =  pred_bi_rev if pred_bi_rev else {}
#
   # print("types")
  #  print(type(pred_tri))
  #  print(type(pred_bi))
  #  print(type(pred_tri_rev))
  #  print(type(pred_bi_rev))
    pred_merged = {k: 0.2*pred_tri.get(k, 0) + 0.2*pred_bi.get(k, 0) + 0.2*pred_tri_rev.get(k, 0) + 0.2*pred_bi_rev.get(k, 0) for k in set(pred_tri) | set(pred_bi) | set(pred_tri_rev) | set(pred_bi_rev)}
   

    # { k: x.get(k, 0) + y.get(k, 0) for k in set(x) | set(y) }
    
    #for pred in pred_tri, pred_bi,pred_tri_rev, pred_bi_rev:
    #    if pred is not None:
    #        for i in range(len(pred)):
    #            word_tuple=pred[i]
    #            pred_merged[word_tuple[0]]=pred_merged[word_tuple[0]]+word_tuple[1];

    return pred_merged

def affin_wb_to_dict(affectfile):
    with open(affectfile, 'rb') as cf:
        f = csv.reader(cf, delimiter='\t')
        wbdict = {row[0]: int(row[1]) for row in f}
    return wbdict

def predictionAffectFilter(predicted, affect):
    filename='AFINN_AFINN-96.txt';
    affectDict=affin_wb_to_dict(filename);
    filename2='AFINN_AFINN-111.txt';
    affectDict2=affin_wb_to_dict(filename2)
    affectDict.update(affectDict2)
    predicted_filtered={}
   # print predicted
    for pred in predicted:
        #remove if not in affectdict
        if pred in affectDict: 
      #  else:
       #     print pred
       #    print affectDict[pred]
   # return predicted
        #if affect=0(negative) and value in affect dict is not, remove
            if affect==0:
                if affectDict[pred]<=0:
            #    print affectDict[pred]
                    affect_val=float(abs(affectDict[pred]))
                    affectFactor=(affect_val/5.0)
                    count=float(predicted[pred])
                    predicted_filtered[pred]=count+0.2*affectFactor;
        #if affect=1(positive) and value in affect dict is not, remove
            elif affect==1:
           # print pred
                if affectDict[pred]>=0:
                    affect_val=float(abs(affectDict[pred]))
                    affectFactor=(affect_val/5.0)
                    count=float(predicted[pred])
                    predicted_filtered[pred]=count*affectFactor;
    return predicted_filtered
    
def mainPredict(vocab,phrase,affect,ngrams_stats_tri, ngrams_stats_bi,ngrams_stats_tri_rev, ngrams_stats_bi_rev):
  #  print "in"
    phrase_token=getPhraseToke(phrase);
  #  print "mp 1"
    phrase_gram=getPhrase(phrase_token);
  #  print "mp2"
  #  print phrase_gram
    pred_tri, pred_bi, pred_tri_rev, pred_bi_rev=predict(vocab, phrase_gram, ngrams_stats_tri, ngrams_stats_bi,ngrams_stats_tri_rev, ngrams_stats_bi_rev);
 #   print "mp3"
   # print pred_tri
  #  print type(pred_tri)
    pred_merged=mergePredictions(pred_tri, pred_bi, pred_tri_rev, pred_bi_rev);
    pred_filtered=predictionAffectFilter(pred_merged, affect);
    return pred_filtered, pred_merged