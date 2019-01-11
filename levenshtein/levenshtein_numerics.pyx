from cpython.string cimport PyString_AsString
from libc.stdlib cimport malloc

cdef extern from "levenshtein.c":
    int _levenshtein(int *s, int len_s, int *t, int len_t)
    int _wagner_fischer(int *s, int len_s, int *t, int len_t)

def levenshtein_cython(s, len_s, t, len_t):
    # base case: empty strings
    if len_s == 0:
        return len_t
    if len_t == 0:
        return len_s
    # test if last characters of the strings match
    if s[len_s-1] == t[len_t-1]:
        cost = 0
    else:
        cost = 1
    # return minimum of delete word from s, delete word from t, and delete word from both 
    return min(levenshtein_cython(s, len_s - 1, t, len_t    ) + 1,
               levenshtein_cython(s, len_s    , t, len_t - 1) + 1,
               levenshtein_cython(s, len_s - 1, t, len_t - 1) + cost);

def levenshtein_c(list phr_lst_s not None, int len_s, list phr_lst_t not None, int len_t):
    cdef int *s = <int*>malloc(len_s * sizeof(int))
    cdef int *t = <int*>malloc(len_t * sizeof(int))
    for i in xrange(len_s):
        s[i] = phr_lst_s[i]
    for j in xrange(len_t):
        t[j] = phr_lst_t[j]
    return _wagner_fischer(<int*> s, len_s, <int*> t, len_t) 
    #return _levenshtein(<int*> s, len_s, <int*> t, len_t) 
