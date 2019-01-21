#ifndef PHRASE_COUNTER_HEADER
#define PHRASE_COUNTER_HEADER

extern int _levenshtein(int *s, int len_s, int *t, int len_t);
extern int _wagner_fischer(int *s, int m, int *t, int n);

#endif
