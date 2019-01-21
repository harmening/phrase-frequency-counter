from counter import counter_s, counter_nos
from counter import analysis
import numpy as np 
from numpy.testing import assert_array_equal
#from levenshtein.levenshtein_numerics import levenshtein_word

def testCounter():
    d = {1: 'A B C D', 2: 'A B C E A B C D', 3: 'A B C D E', \
        4: 'C E A B', 5: 'A E E E', 6: 'B C B C', 7: 'C B E E', \
        8: 'B C E', 9: 'E A B C E'}
    matrix_s = analysis(counter_s(d))
    matrix_nos = analysis(counter_nos(d))
    assert_array_equal(matrix_s, [[4, 4, 9], [3, 1, 1], [2, 3, 5], \
                                  [1, 2, 2]])
    assert_array_equal(matrix_nos, [[4, 4, 9], [3, 1, 1], [2, 3, 5], \
                                    [1, 2, 2]])


def testCountOnlyOneOfSamePhrasePerMessage():
    matrix_s = analysis(counter_s({1: 'This is a second This is a second'}))
    matrix_nos = analysis(counter_nos({1: 'This is a second This is a second'}))
    assert_array_equal(matrix_s[0], [4, 1, 1])
    assert_array_equal(matrix_nos[0], [4, 1, 1])
    
def testNotCountSinglePhrase():
    matrix_s = analysis(counter_s({1: 'This is a long phrase', 2: 'This is a'}))
    assert_array_equal(matrix_s[0], [3, 1, 2])
    matrix_s = analysis(counter_s({1: 'This is a long phrase', 2: 'A new Phrase', \
            3: 'This is a long phrase'}))
    assert_array_equal(matrix_s[2], [3, 0, 0])
    matrix_nos = analysis(counter_nos({1: 'This is a long phrase', 2: 'This is a'}))
    assert_array_equal(matrix_nos[0], [3, 1, 2])
    matrix_nos = analysis(counter_nos({1: 'This is a long phrase', 2: 'A new Phrase', \
            3: 'This is a long phrase'}))
    assert_array_equal(matrix_nos[2], [3, 0, 0])

def testNotCountIfFullyMarked():
    matrix_s = analysis(counter_s({1: 'This is a phrase', 2: 'This is a phrase', \
            3: 'Here is a', 4: 'Here is a sentence'}))
    matrix_nos = analysis(counter_s({1: 'This is a phrase', 2: 'This is a phrase', \
            3: 'Here is a', 4: 'Here is a sentence'}))
    # Dont count 'is a', cause it's marked in every message
    assert_array_equal(matrix_s[2], [2, 0, 0])
    assert_array_equal(matrix_nos[2], [2, 0, 0])

def testCountSinglePhraseIfInLongerPhrase():
    matrix_s = analysis(counter_s({1: 'This is a long phrase', 2: 'This is a', \
            3: 'This is a long phrase'}))
    matrix_nos = analysis(counter_nos({1: 'This is a long phrase', 2: 'This is a', \
            3: 'This is a long phrase'}))
    assert_array_equal(matrix_s[2], [3, 1, 1])
    assert_array_equal(matrix_nos[2], [3, 1, 1])

def testSingleWords():
    tuples_s = counter_s({1: 'This is a sentence with no word repetition at all.'})
    tuples_nos = counter_nos({1: 'This is a sentence with no word repetition at all.'})
    assert_array_equal(analysis(tuples_s).shape, (0, 3))
    assert_array_equal(analysis(tuples_nos).shape, (0, 3))

def testSentenceSplitting():
    d = {1: 'Here it is. A phrase, but Mr. Smith said this is an' +
        ' example of only one phrase.', 2: 'Although it is a phrase here again.', \
        3: 'It is a phrase. Mr Smith said it.'}
    matrix_s = analysis(counter_s(d))
    assert_array_equal(matrix_s[0], [4, 1, 2]) # it is a phrase
    assert_array_equal(matrix_s[1], [3, 1, 2]) # Mr Smith said

def testNoSentenceSplitting():
    d = {1: 'Here it is. A phrase, but Mr. Smith said this is an' +
        ' example of only one phrase.', 2: 'Although it is a phrase here again.', \
        3: 'It is a phrase. Mr Smith said it.'}
    matrix_nos = analysis(counter_nos(d))
    # Different results for no-sentence-splitting!
    assert_array_equal(matrix_nos[0], [4, 1, 3]) # it is a phrase
    assert_array_equal(matrix_nos[1], [3, 1, 2]) # Mr Smith said


#def testLevenshteinWord():
#    assert levenshtein_word("sport", "support") != -1
