from counter import counter_sentences as counter_s
from counter import counter_nosentences as counter_nos
import numpy as np 
from numpy.testing import assert_array_equal


def testCounter():
    d = {1: 'A B C D', 2: 'A B C E A B C D', 3: 'A B C D E', \
        4: 'C E A B', 5: 'A E E E', 6: 'B C B C', 7: 'C B E E', \
        8: 'B C E', 9: 'E A B C E'}
    matrix_s = counter_s(d)[0]
    matrix_nos = counter_nos(d)[0]
    assert_array_equal(matrix_s, [[4, 4, 9], [3, 1, 1], [2, 3, 5], \
                                  [1, 2, 2]])
    assert_array_equal(matrix_nos, [[4, 4, 9], [3, 1, 1], [2, 3, 5], \
                                    [1, 2, 2]])


def testCountOnlyOneOfSamePhrasePerMessage():
    matrix_s = counter_s({1: 'This is a second This is a second'})[0]
    matrix_nos = counter_nos({1: 'This is a second This is a second'})[0]
    assert_array_equal(matrix_s[0], [4, 1, 1])
    assert_array_equal(matrix_nos[0], [4, 1, 1])
    
def testNotCountSinglePhrase():
    matrix_s = counter_s({1: 'This is a long phrase', 2: 'This is a'})[0]
    assert_array_equal(matrix_s[0], [3, 1, 2])
    matrix_s = counter_s({1: 'This is a long phrase', 2: 'A new Phrase', \
            3: 'This is a long phrase'})[0]
    assert_array_equal(matrix_s[2], [3, 0, 0])
    matrix_nos = counter_nos({1: 'This is a long phrase', 2: 'This is a'})[0]
    assert_array_equal(matrix_nos[0], [3, 1, 2])
    matrix_nos = counter_nos({1: 'This is a long phrase', 2: 'A new Phrase', \
            3: 'This is a long phrase'})[0]
    assert_array_equal(matrix_nos[2], [3, 0, 0])

def testNotCountIfFullyMarked():
    matrix_s = counter_s({1: 'This is a phrase', 2: 'This is a phrase', \
            3: 'Here is a', 4: 'Here is a sentence'})[0]
    matrix_nos = counter_s({1: 'This is a phrase', 2: 'This is a phrase', \
            3: 'Here is a', 4: 'Here is a sentence'})[0]
    # Dont count 'is a', cause it's marked in every message
    assert_array_equal(matrix_s[2], [2, 0, 0])
    assert_array_equal(matrix_nos[2], [2, 0, 0])

def testCountSinglePhraseIfInLongerPhrase():
    matrix_s = counter_s({1: 'This is a long phrase', 2: 'This is a', \
            3: 'This is a long phrase'})[0]
    matrix_nos = counter_nos({1: 'This is a long phrase', 2: 'This is a', \
            3: 'This is a long phrase'})[0]
    assert_array_equal(matrix_s[2], [3, 1, 1])
    assert_array_equal(matrix_nos[2], [3, 1, 1])

def testSingleWords():
    matrix_s = counter_s({1: 'This is a sentence with no word repetition at all.'})[0]
    matrix_nos = counter_nos({1: 'This is a sentence with no word repetition at all.'})[0]
    assert_array_equal(matrix_s.shape, (0, 3))
    assert_array_equal(matrix_nos.shape, (0, 3))

def testSentenceSplitting():
    d = {1: 'Here it is. A phrase, but Mr. Smith said this is an' +
        ' example of only one phrase.', 2: 'Although it is a phrase here again.', \
        3: 'It is a phrase. Mr Smith said it.'}
    matrix_s = counter_s(d)[0]
    assert_array_equal(matrix_s[0], [4, 1, 2]) # it is a phrase
    assert_array_equal(matrix_s[1], [3, 1, 2]) # Mr Smith said

def testNoSentenceSplitting():
    d = {1: 'Here it is. A phrase, but Mr. Smith said this is an' +
        ' example of only one phrase.', 2: 'Although it is a phrase here again.', \
        3: 'It is a phrase. Mr Smith said it.'}
    matrix_nos = counter_nos(d)[0]
    # Different results for no-sentence-splitting!
    assert_array_equal(matrix_nos[0], [4, 1, 3]) # it is a phrase
    assert_array_equal(matrix_nos[1], [3, 1, 2]) # Mr Smith said
