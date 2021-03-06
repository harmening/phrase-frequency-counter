from levenshtein_numerics import levenshtein_c, levenshtein_cython
import numpy as np
import pickle, os, gzip, string

def levenshtein_phrase_distance(phr_s, phr_t, CYTHON=False):
    s, t = phr_s.split(), phr_t.split()
    # Create dictionary and assign each word to a unique int
    d = {}
    idx = 1
    # Translate phr_s and phr_t in int-language
    s1, s2 = [], []
    for w1 in s:
        if w1 not in d.keys():
            d[w1]=idx
            idx+=1
        s1.append(d[w1])
    for w2 in t:
        if w2 not in d.keys():
            d[w2]=idx
            idx+=1
        s2.append(d[w2])
    # aviod calculation?
    aviod_calc = True
    for word in s:
        if word in t:
            avoid_calc = False
    # for completely different phrases: distance = num of words of longer phrase
    if avoid_calc:
        return max(len(s), len(t))
    else:
        if CYTHON:
            return levenshtein_cython(s1, len(s), s2, len(t))
        else:
            return levenshtein_c(s1, len(s), s2, len(t))
