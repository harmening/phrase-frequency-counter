from cpython.string cimport PyString_AsString
from libc.stdlib cimport malloc, free

# Linked List Struct for information of collected phrases
ctypedef struct _LinkedListStruct:
    int *phrase
    long *ids
    int num_ids
    _LinkedListStruct*next

cdef extern from "src_numerics.c":
    _LinkedListStruct* _pcounter(int *mess_len, long num_messages,
            int **messages, int **mark, long *ids, int phr_len)
    _LinkedListStruct* _pcounter_sent(int *mess_len, int *sent_len,
            long num_messages, long num_sentences, 
            int **sentences, int **mark, long *ids, int phr_len)



def counter_c(list messages_as_digits, list mids_as_digits, int max_N_w):

    # allocate storage for passing messages and ids to external c code
    cdef:
        long num_messages = len(messages_as_digits)
        int **messages = <int**> malloc(num_messages * sizeof(int *))
        int **mark = <int**> malloc(num_messages * sizeof(int *))
        int i, j, phr_len
        long *ids = <long*> malloc(num_messages * sizeof(long))
        int *mess_len = <int*> malloc(num_messages * sizeof(int))
  
    # Fill with information from python code
    for i in range(num_messages):
        ids[i] = mids_as_digits[i]
        mess_len[i] = len(messages_as_digits[i])
        messages[i] = <int*> malloc(mess_len[i] * sizeof(int))
        mark[i] = <int*> malloc(mess_len[i] * sizeof(int))
        for j in range(mess_len[i]):
            messages[i][j] = messages_as_digits[i][j]
            mark[i][j] = 0


    del messages_as_digits, mids_as_digits
    # Results (=tuples) are returned
    cdef _LinkedListStruct *collected

    tuples = []
    for phr_len in range(max_N_w, 0, -1):

        # Call c function
        collected = _pcounter(<int*> mess_len, num_messages, <int**> messages,
                <int**> mark, <long*> ids, phr_len)

        # Collect results (tuples) and free space
        while collected is not NULL:
            this_phrase = []
            this_id = []
            for j in range(collected.num_ids):
                this_id.append(collected.ids[j])
            free(collected.ids)
            for j in range(phr_len):
                this_phrase.append(collected.phrase[j])
            free(collected.phrase)
            tuples.append([this_phrase, this_id])
            collected = collected.next
        free(collected)

    for i in range(num_messages):
        free(messages[i])
        free(mark[i])
    free(messages)
    free(ids)
    free(mess_len)

    return tuples



def counter_c_sent(list sentences_as_digits, list mids_as_digits,
                   long num_sentences, int max_N_w):

    # allocate storage for passing messages and ids to external c code
    cdef:
        long num_messages = len(mids_as_digits)
        int **sentences = <int**> malloc(num_sentences * sizeof(int *))
        int **mark = <int**> malloc(num_sentences * sizeof(int *))
        int i, j, w, s, phr_len
        long *ids = <long*> malloc(num_messages * sizeof(long))
        int *mess_len = <int*> malloc(num_messages * sizeof(int))
        int *sent_len = <int*> malloc(num_sentences * sizeof(int))

    # Fill with information from python code
    s = 0
    for i in range(num_messages):
        ids[i] = mids_as_digits[i]
        mess_len[i] = len(sentences_as_digits[i])
        for j in range(mess_len[i]):
            sent_len[s] = len(sentences_as_digits[i][j])
            sentences[s] = <int*> malloc(sent_len[s] * sizeof(int))
            mark[s] = <int*> malloc(sent_len[s] * sizeof(int))
            for w in range(sent_len[s]):
                sentences[s][w] = sentences_as_digits[i][j][w]
                mark[s][w] = 0
            s += 1
     
    del sentences_as_digits, mids_as_digits

    # Results (=tuples) are returned
    #cdef _LinkedListStruct *collected, *temp
    cdef _LinkedListStruct *collected = NULL
    cdef _LinkedListStruct *temp = NULL

    tuples = []
    for phr_len in range(max_N_w, 0, -1):
        # Call c function
        collected = _pcounter_sent(<int*> mess_len, <int*> sent_len,
                num_messages, num_sentences,
                <int**> sentences, <int**> mark, <long*> ids, phr_len)

        while collected is not NULL:
            this_phrase = []
            this_id = []
            for j in range(collected.num_ids):
                this_id.append(collected.ids[j])
            free(collected.ids)
            for j in range(phr_len):
                this_phrase.append(collected.phrase[j])
            free(collected.phrase)
            tuples.append([this_phrase, this_id])
            temp = collected.next
            free(collected)
            collected = temp
        free(temp)

    for i in range(num_sentences):
        free(sentences[i])
        free(mark[i])
    free(sentences)
    free(ids)
    free(mess_len)
    free(sent_len)

    return tuples
