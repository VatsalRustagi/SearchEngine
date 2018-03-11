from nltk import stem
from math import log10
import re

def Stemmer(words):
    stemmer = stem.SnowballStemmer("english", True)
    return [stemmer.stem(w) for w in words]

def calculate_tfidf(tf,df, TotalDocuments):
    a =1.0 + log10(tf)
    b= log10(TotalDocuments/df)
    return round((a*b),2)

def simplifyText(text):
    return re.sub('[^a-zA-Z0-9]+', " ", text.strip()).strip()