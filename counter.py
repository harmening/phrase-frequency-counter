from matplotlib import pyplot as plt
import numpy as np
import string, re
import spacy
nlp = spacy.load('en')

from numerics import counter_c, counter_c_sent

# chose if counting happens within each  SENTENCE or DOCUMENT:
LEVEL = 'SENTENCE' # 'DOCUMENT'


def hirsch_index(tuples):
    try:
        phr_len = len(tuples[0][0].split())
    except:
        phr_len = 0
    h = {}
    for i in range(len(tuples)):
        if len(tuples[i][0].split()) != phr_len:
            phr_len = len(tuples[i][0].split())
        num_of_ids = 0
        for j in range(len(tuples[i][1])):
            num_of_ids += len(tuples[i][1][j])
        h[tuples[i][0]] = min(phr_len, num_of_ids)
    sorted_h = sorted(h.items(), key=operator.itemgetter(1))
    l = len(sorted_h)
    for i in range(1,l):
        if sorted_h[-i][1] < i:
            hidx = i-1
            break
    return hidx

def plot_matrix(matrix):
    plt.subplot(1, 2, 1); plt.gca().invert_xaxis()
    plt.plot(matrix[:,0],matrix[:,1])
    plt.xlabel("Phrase length"); plt.ylabel("Number of different phrases")
    plt.subplot(1, 2, 2); plt.gca().invert_xaxis()
    plt.plot(matrix[:,0],matrix[:,2])
    plt.xlabel("Phrase length"); plt.ylabel("Appearence of all phrases")
    plt.savefig('phrases.png')

#small helpers
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
            print(tup)
            if len(tup[1]) > 0:
                # 2nd entry: number of different phrases with this phr_len
                matrix[max_phr_len-len(tup[0].split())][1] += 1
                # 3rd entry: number of all phrase-appearences with this phr_len
                num_of_ids = 0
                for j in range(len(tup[1])):
                    num_of_ids += len(tup[1][j])
                matrix[max_phr_len-len(tup[0].split())][2] += num_of_ids
    return matrix

def counter_nos(mails):
    max_num_words, current_word_idx, current_id_idx = 0, 0, 0
    word2idx, id2idx = {}, {}
    index2word, index2id, messages_as_digits, mids_as_digits = [], [], [], []
    # Transform messages of words into sequence of digits
    for m, mid in iterate(mails.keys()):
        mail = mails[mid].lower()
        mail = re.sub(r'[^\w\s]','',mail)
        message = mail.split()
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


def counter_s(mails):
    current_word_idx, current_id_idx, num_sentences, max_num_words = 0, 0, 0, 0
    word2idx, id2idx = {}, {}
    index2word, index2id, sentences_as_digits, mids_as_digits = [], [], [], []
    #Preprocessing
    sentences = []
    for m, mid in iterate(mails.keys()):
        sentences_as_digits.append([])
        # splitting sentences
        doc = nlp(unicode(mails[mid], "utf-8"))
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
        if m not in id2idx:
            id2idx[m] = current_id_idx
            current_id_idx += 1
            index2id.append(m)
        mids_as_digits.append(id2idx[m])
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



if __name__ == '__main__':
    import sys
    if (len(sys.argv) == 2 and sys.argv[1] and len(sys.argv[1]) > 1 ):
        pass
    else:
        print("Run the script with python counter.py <<path_to_mailbox_folder>>")
        sys.exit(0)
    path = sys.argv[1]

    mails = []
    for mail in os.listdir(path):
        mails.append(mail)
    for mail in mails:
        # Sentence level
        if LEVEL == 'SENTENCE':
            tuples = counter_s(mail)
            matrix = analysis(tuples)
        # Message/document level
        elif LEVEL == 'DOCUMENT':
            messages = {}
            #Preprocessing
            for m, this_mail in enumerate(mail):
                messages[m] = this_mail.lower()
                for punctuation in string.punctuation:
                    messages[m] = messages[m].replace(punctuation,"")
            tuples = counter_nos(messages)
            matrix = analysis(tuples)
        else:
            tuples = matrix = None

    hirsch_idx = hirsch_index(tuples)
    plot_matrix(matrix) 
