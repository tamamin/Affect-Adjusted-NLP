# Affect-Adjusted-NLP
Creating an Affect-Adjusted NLP Model using NLTK for the humanoid Pepper robot. This is the initial version of the open-source NLP generator created by Tamara Amin for the paper 'The Impact of Humanoid Affect Expression on Human Behavior in a Game-Theoretic Setting'

Citation: Aaron Roth*, Umang Bhatt*, Tamara Amin*, Afsaneh Doryab, Fei Fang, & Manuela Veloso. The Impact of Humanoid Affect Expression on Human Behavior in Game-Theoretic Setting. IJCAI 2018 Workshop on Humanizing Artificial Intelligence. Stockholm, Sweden.

READ PAPER: https://arxiv.org/pdf/1806.03671.pdf

This code will require the following modules to be installed:nltk, math, re, collections, csv, unicodedata
You will also need to download the AFINN Affect Dictionary.

Execute the code as follows:

1. run NLP_Pepper
2. run main_ngram_Train - WARNING: this could take a while
3. run NLP_Predictions
4. run main_ngram_Predict (NOTE: use the format in the comments:0=negative affect, 1 = positive affect - but replace phrases. It will return the sorted top 10.


