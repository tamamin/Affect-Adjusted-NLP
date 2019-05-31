# -*- coding: utf-8 -*-
"""
Created on Tue May 01 20:28:39 2018

@author: Tamara Amin
"""
phrase="You make me want to"
print phrase
# should we add fisher
#should we add synonyms

affect=1 ;
print "Positive affect:"
pred_filtered, pred_merged=mainPredict(vocab,phrase,affect,ngrams_stats_tri, ngrams_stats_bi,ngrams_stats_tri_rev, ngrams_stats_bi_rev);
sorted_prediction=sorted(pred_filtered.items(), reverse=True, key=lambda x: x[1]);
i=0
for i in range(0,10):
    print sorted_prediction[i][0], np.log(sorted_prediction[i][1])
    

affect=0 ;
print "Negative affect:"
pred_filtered, pred_merged=mainPredict(vocab,phrase,affect,ngrams_stats_tri, ngrams_stats_bi,ngrams_stats_tri_rev, ngrams_stats_bi_rev);
sorted_prediction=sorted(pred_filtered.items(), reverse=True, key=lambda x: x[1]);
i=0
for i in range(0,10):
    print sorted_prediction[i][0], np.log(sorted_prediction[i][1])

print "_____"
'''
phrase= "You seem like a very _ person"
print phrase

affect=1 ;
print "Positive affect:"
pred_filtered, pred_merged=mainPredict(phrase,affect,ngrams_stats_tri, ngrams_stats_bi,ngrams_stats_tri_rev, ngrams_stats_bi_rev);
sorted_prediction=sorted(pred_filtered.items(), reverse=True, key=lambda x: x[1]);

for i in range(0,10):
    print sorted_prediction[i][0], np.log(sorted_prediction[i][1])phrase= "This game is a _ experiment"



affect=0 ;
print "Negative affect:"
pred_filtered, pred_merged=mainPredict(phrase,affect,ngrams_stats_tri, ngrams_stats_bi,ngrams_stats_tri_rev, ngrams_stats_bi_rev);
sorted_prediction=sorted(pred_filtered.items(), reverse=True, key=lambda x: x[1]);
print phrase
for i in range(0,10):
    print sorted_prediction[i][0], np.log(sorted_prediction[i][1])
print "_____"
'''