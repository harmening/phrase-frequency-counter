import numpy as np
import string
import spacy
nlp = spacy.load('en')
try: 
    #import pyximport; pyximport.install()
    from numerics import counter_c, counter_c_sent
    CYTHON = True
except:
    CYTHON = False


def get_substrings(input_string, substring_length):
    lst = input_string.split()
    return [' '.join(lst[i:i+substring_length]) for i in
            range(len(lst)-substring_length+1)]

def get_substrings_list(input_list, substring_length):
    lst = []
    for i in input_list:
        for j in get_substrings(i, substring_length):
            lst.append(j)
    return lst




########## Analysis ##########
def analysis(tuples):
    try:
        max_phr_len = len(tuples[0][0].split())
    except:
        max_phr_len = 0
    # create matrix
    matrix = np.zeros((max_phr_len, 3), dtype=int)
    if max_phr_len > 0:
        # 1st entry: phrase length
        for i in range(max_phr_len):
            matrix[i][0] = max_phr_len-i

        for tup in tuples:
            if len(tup[1]) > 0:
                # 2nd entry: number of different phrases with this phr_len
                matrix[max_phr_len-len(tup[0].split())][1] += 1
                # 3rd entry: number of all phrase-appearences with this phr_len
                num_of_ids = 0
                for j in range(len(tup[1])):
                    num_of_ids += len(tup[1][j])
                matrix[max_phr_len-len(tup[0].split())][2] += num_of_ids

    return matrix




def counter_nos_c(messages_id):
    max_num_words, current_word_idx, current_id_idx = 0, 0, 0
    word2idx, id2idx = {}, {}
    index2word, index2id, messages_as_digits, mids_as_digits = [], [], [], []
    # Transform messages of words into sequence of digits
    for mid in messages_id.keys():
        message = messages_id[mid].split()
        if len(message) > max_num_words:
            max_num_words = len(message)

        mess_as_digits = []
        for word in message:
            if word not in word2idx:
                word2idx[word] = current_word_idx
                current_word_idx += 1
                index2word.append(word)
            mess_as_digits.append(word2idx[word])
        messages_as_digits.append(mess_as_digits)
   
        #ids_as_digits = []
        if mid not in id2idx:
            id2idx[mid] = current_id_idx
            current_id_idx += 1
            index2id.append(mid)
        mids_as_digits.append(id2idx[mid])
    
    tuples_digits = counter_c(messages_as_digits, mids_as_digits, max_num_words)
    tuples = []
    # Retransformation
    for tup in tuples_digits:
        phrase = []
        for word_idx in tup[0]:
            phrase.append(index2word[word_idx])
        ids = []
        for id_idx in tup[1]:
            ids.append(index2id[id_idx])
        tuples.append([" ".join(phrase), [ids]])

    return tuples




def counter_nos_p(messages_id):
    messages = messages_id.values()
    max_num_words = 0   # largest number of words in sentence of all messages
    words = []  # store words
    mark = []   # corresponding marking of words
    tuples = []     # for later creation of matrix; contains phrase and count
    
    # Revert messages_id to have message-ids as keys
    ids = {}
    for k, v in messages_id.iteritems():
        ids[v] = ids.get(v, [])
        ids[v].append(k)

    num_messages = len(messages)  # number of input texts/messages/emails


    ########## Cleaning and Storing Data ##########
    # store all words of all messages and create for each word boolean if marked
    for m in range(num_messages):
        if len(messages[m].split()) > max_num_words:
            max_num_words = len(messages[m].split())
        words.append(messages[m].split())
        mark.append([False for i in range(len(words[m]))])


    # search for recurring phrases, starting with longest phrases, decreasing
    for phr_len in range(max_num_words, 0, -1):
        ########## Create search-phrases list ##########
        phrases = [] 
        # get all possible phrases with this phr_len
        for m in range(num_messages):
            for i in get_substrings(messages[m], phr_len):
                if i not in phrases:
                    phrases.append(i)


        ########## Search phrases in all messages ##########
        # loop over all possible phrases from this sentence
        collected_phrases = []
        for this_phrase in phrases:
            occurrence = 0
            count_ids = []
            
            # search in all messages for this_phrase
            for m in range(num_messages):
                # create list of all possible phrases in text we need to
                # compare our phrase with

                # check if phrase already counted in this text
                already_counted_in_t = False
                N_w = len(messages[m].split())   # number of words in message
                # max possible number of phrases in this message
                poss_num_phr = N_w - phr_len + 1
                if poss_num_phr > 0 and this_phrase in messages[m]:
                    words_as_phr = []
                    for i in get_substrings(messages[m], phr_len):
                        words_as_phr.append(i) 

                    # get all first indices of all appearences of this_phrase
                    idx0 = [i for i in range(len(words_as_phr))
                            if words_as_phr[i] == this_phrase]

                    # loop over all appearences
                    for index0 in idx0:
                        occurrence += 1

                        # check if all words are already marked
                        marked = True
                        for p in range(phr_len):
                            marked *= mark[m][index0+p]


                        # if phrase not fully marked and not already counted
                        if not bool(marked) and not already_counted_in_t:
                            try:
                                count_ids.append(ids[messages[m]])
                            except:
                                count_ids.append("id-placeholder")
                                print("Not possible to find id in "+\
                                "mailbox %s to message %s." % mail, \
                                messages[m])
                            already_counted_in_t= True

                                   

            # only collect phrase if it appears more than once
            if occurrence >= 2 and len(count_ids) >= 1:
                #and phr_len < init_max_m: # don't count double massages
                collected_phrases.append(this_phrase)
                tuples.append([this_phrase, count_ids])



        ########## Mark words of phrases in all messages ##########
        # mark all words of all collected phrases of phr_len in all messages
        for this_phrase in collected_phrases:
            for tt in range(num_messages):
                if this_phrase in messages[tt]:

                    # calculate all possible phrases in text with phr_len
                    words_as_phr = []
                    N_w = len(messages[tt].split())
                    poss_num_phr = N_w - phr_len + 1
                    if poss_num_phr > 0:
                        for i in get_substrings(messages[tt], phr_len):
                            words_as_phr.append(i) 
                        for i in range(phr_len-1):
                            words_as_phr.append(' ')
                    else:
                        for i in range(N_w):
                            words_as_phr.append(' ')

                    # get first indices of all appearences of phrase in text
                    idx0 = [i for i in range(len(words_as_phr))
                            if words_as_phr[i] == this_phrase]

                     
                    # mark all words of phrase
                    for index0 in idx0:
                        for p in range(phr_len):
                            mark[tt][index0+p] = True

    return tuples




def counter_s_c(messages_id):
    current_word_idx, current_id_idx, num_sentences, max_num_words = 0, 0, 0, 0
    word2idx, id2idx = {}, {}
    index2word, index2id, sentences_as_digits, mids_as_digits = [], [], [], []

    #Preprocessing
    ids = messages_id.keys()
    sentences = []
    for m in range(len(ids)):
        sentences_as_digits.append([])

        # splitting sentences
        doc = nlp(unicode(messages_id.values()[m], "utf-8"))
        sentences.append([sent.string.strip().encode('utf-8').strip() \
                for sent in doc.sents])
        for s in range(len(sentences[m])):
            num_sentences += 1
            # strip punctuation for phrase cleaning
            sentences[m][s] = sentences[m][s].lower()
            for punctuation in string.punctuation:
                sentences[m][s] = sentences[m][s].replace(punctuation,"")
            if len(sentences[m][s].split()) > max_num_words:
                max_num_words = len(sentences[m][s].split())
       
            # Transform messages of words into sequence of digits
            sentence = sentences[m][s].split()
            sent_as_digits = []
            for word in sentence:
                if word not in word2idx:
                    word2idx[word] = current_word_idx
                    current_word_idx += 1
                    index2word.append(word)
                sent_as_digits.append(word2idx[word])
            sentences_as_digits[m].append(sent_as_digits)


        mid = ids[m]
        if mid not in id2idx:
            id2idx[mid] = current_id_idx
            current_id_idx += 1
            index2id.append(mid)
        mids_as_digits.append(id2idx[mid])

    
    tuples_digits = counter_c_sent(sentences_as_digits, mids_as_digits,
                                   num_sentences, max_num_words)


    # Retransformation
    tuples = []
    for tup in tuples_digits:
        phrase = []
        for word_idx in tup[0]:
            phrase.append(index2word[word_idx])
        ids = []
        for id_idx in tup[1]:
            ids.append(index2id[id_idx])
        tuples.append([" ".join(phrase), [ids]])
    
    return tuples




def counter_s_p(messages_id):
    #Preprocessing
    ids = messages_id.keys()
    sentences = []
    max_num_words = 0
    for m in range(len(ids)):

        # splitting sentences
        doc = nlp(unicode(messages_id.values()[m], "utf-8"))
        sentences.append([sent.string.strip().encode('utf-8').strip() \
                for sent in doc.sents])
        for s in range(len(sentences[m])):
            # strip punctuation for phrase cleaning
            sentences[m][s] = sentences[m][s].lower()
            for punctuation in string.punctuation:
                sentences[m][s] = sentences[m][s].replace(punctuation,"")
            if len(sentences[m][s].split()) > max_num_words:
                max_num_words = len(sentences[m][s].split())


    messages = messages_id.values()
    # Revert messages_id to trace ids from messages
    for mid in messages_id.keys():
        messages_id[mid] = messages_id[mid].lower()
        for punctuation in string.punctuation:
            messages_id[mid] = messages_id[mid].replace(punctuation,"")
    ids = {}
    for k, v in messages_id.iteritems():
        ids[v] = ids.get(v, [])
        ids[v].append(k)

    
    num_messages = len(messages)  # number of input texts/messages/emails
    max_num_words = 0   # largest number of words in sentence of all messages
    sentences = []  # store sentences
    words = []  # store words
    mark = []   # corresponding marking of words
    tuples = []     # for later creation of matrix; contains phrase and count


    ########## Cleaning and Storing Data ##########
    # store all words of all messages and create for each word a bool if marked
    for m in range(num_messages):
        """
        if num_messages >= 1000:
            if m % int(num_messages/1000) == 0:
                print(str(round(float(m)/num_messages*100, 0))+"%")
        """
        # splitting sentences
        doc = nlp(unicode(messages[m], "utf-8"))
        sentences.append([sent.string.strip().encode('utf-8').strip() \
                for sent in doc.sents])
        messages[m] = messages[m].lower()
        # strip punctuation for text cleaning
        for punctuation in string.punctuation:
            messages[m] = messages[m].replace(punctuation,"")
        message = ""
        for s in range(len(sentences[m])):
            # strip punctuation for phrase cleaning
            for punctuation in string.punctuation:
                sentences[m][s] = sentences[m][s].lower()
                sentences[m][s] = sentences[m][s].replace(punctuation,"")
            message = message + sentences[m][s] + " "
            if len(sentences[m][s].split()) > max_num_words:
                max_num_words = len(sentences[m][s].split())
        
        words.append(message.split())
        mark.append([False for i in range(len(words[m]))])
   

    """
    # Store results
    with open('sentences.py', 'w') as f:
        f.write('sentences = %s' % sentences)
    with open('messages.py', 'w') as f:
        f.write('messages = %s' % messages)
    with open('words.py', 'w') as f:
        f.write('words = %s' % words)
    with open('mark.py', 'w') as f:
        f.write('mark = %s' % mark)
    """


    for phr_len in range(max_num_words, 0, -1):
        ##for i in collected_phrases:
        ##    all_collected_phrases.append(i)
        collected_phrases = []
        # get subphrases of already collected phrases
        ##already_collected = get_substrings_list(all_collected_phrases, phr_len)
        # get all possible phrases with this phr_len
        phrases = [] 
        for m in range(num_messages):
            for s in range(len(sentences[m])):
                """
                #def get_substrings(input_string, substring_length):
                input_string = sentences[m][s]
                substring_length = phr_len
                lst = input_string.split()
                fun_return = [' '.join(lst[i:i+substring_length])
                              for i in range(len(lst)-substring_length+1)]
                for i in fun_return:
                """
                for i in get_substrings(sentences[m][s], phr_len):
                    if i not in phrases:## and i not in already_collected:
                        phrases.append(i)



        ########## Search phrases in all messages ##########
        # loop over all possible phrases from this sentence
        for this_phrase in phrases:
            occurrence = 0
            count_ids = []
            # if exact phrase not already processed
            #if this_phrase not in collected_phrases:
                #if this_phrase in messages[m]:   # necessary?

            # search in all sentences for phrases
            for m in range(num_messages):
                # create list of all possible phrases in text we
                # need to compare our phrase with
                words_in_text = 0    # number of words in all sentences of text
                # check if phrase already counted in this text
                already_counted_in_t = False
                for s in range(len(sentences[m])):
                    N_w = len(sentences[m][s].split())   # number of words in sentence
                    # max possible number of phrases in this sentence
                    poss_num_phr = N_w - phr_len + 1
                    if poss_num_phr > 0 and this_phrase in sentences[m][s]:
                        words_as_phr = []
                        """
                        for i in get_substrings(sentences[m][s], phr_len):
                            words_as_phr.append(i) 
                        """
                        for i in range(words_in_text, words_in_text+poss_num_phr):
                            words_as_phr.append(' '.join(words[m][i:i+phr_len]))
                           
                        # get all first indices of all appearences of phrase in text
                        idx0 = [i for i in range(len(words_as_phr))
                                if words_as_phr[i] == this_phrase]

                        # loop over all appearences
                        for index0 in idx0:
                            occurrence += 1

                            # check if all words are already marked
                            marked = True
                            for p in range(phr_len):
                                marked *= mark[m][words_in_text+index0+p]


                            # if phrase not fully marked and not already counted
                            if not bool(marked) and not already_counted_in_t:
                                try:
                                    count_ids.append(ids[messages[m]])
                                except:
                                    count_ids.append("id-placeholder")
                                    print("Not possible to find id in "+\
                                    "mailbox %s to message %s." % mail, \
                                    messages[m])
                                already_counted_in_t= True

                    words_in_text += N_w
                                   

            # only collect phrase if it appears more than once
            if occurrence >= 2 and len(count_ids) >= 1:
                #and phr_len < init_max_m: # don't count double massages
                collected_phrases.append(this_phrase)
                tuples.append([this_phrase, count_ids])



        ########## Mark words of phrases in all messages ##########
        # mark all words of all collected phrases of phr_len in all messages
        for this_phrase in collected_phrases:
            for tt in range(num_messages):
                if this_phrase in messages[tt]:

                    # calculate all possible phrases in text with phr_len
                    words_as_phr = []
                    for ss in range(len(sentences[tt])):
                        N_w = len(sentences[tt][ss].split())
                        poss_num_phr = N_w - phr_len + 1
                        if poss_num_phr > 0:
                            """
                            #def get_substrings(input_string, substring_length):
                            input_string = sentences[tt][ss]
                            substring_length = phr_len
                            lst = input_string.split()
                            fun_return = [' '.join(lst[i:i+substring_length])
                                          for i in range(len(lst)-substring_length+1)]
                            for i in fun_return:
                            """
                            for i in get_substrings(sentences[tt][ss], phr_len):
                                words_as_phr.append(i) 
                            for i in range(phr_len-1):
                                words_as_phr.append(' ')
                        else:
                            for i in range(N_w):
                                words_as_phr.append(' ')

                    # get first indices of all appearences of phrase in text
                    idx0 = [i for i in range(len(words_as_phr))
                            if words_as_phr[i] == this_phrase]

                     
                    # mark all words of phrase
                    for index0 in idx0:
                        for p in range(phr_len):
                            mark[tt][index0+p] = True

    return tuples






def counter_nosentences(messages_id):
    #Preprocessing
    for mid in messages_id.keys():
        messages_id[mid] = messages_id[mid].lower()
        for punctuation in string.punctuation:
            messages_id[mid] = messages_id[mid].replace(punctuation,"")
    
    if CYTHON:
        tuples = counter_nos_c(messages_id)
    else:
        tuples = counter_nos_p(messages_id)

    matrix = analysis(tuples)
    return matrix, tuples



def counter_sentences(messages_id):
    if CYTHON:
        tuples = counter_s_c(messages_id)
    else:
        tuples = counter_s_p(messages_id)

    matrix = analysis(tuples)
    return matrix, tuples



if __name__ == '__main__':
    num_cpus = mp.cpu_count()
    print(num_cpus)
    mails = []
    for mail in os.listdir(path):
        mails.append(mail)
   
    p = mp.Pool(num_cpus)
    p.map(counter_sentences, mails)
    #p.map(counter_nosentences, mails)