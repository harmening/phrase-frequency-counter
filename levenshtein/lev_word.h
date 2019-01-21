#ifndef PHRASE_COUNTER_HEADER
#define PHRASE_COUNTER_HEADER

extern int _levenshtein1(char *str1, char *str2);
extern int _levenshtein2(char *str1, char *str2);
extern int _wagner_fischer_word(char *str1, int str1len, char *str2, int str2len);

#endif
