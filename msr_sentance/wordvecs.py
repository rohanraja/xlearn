import numpy as np
# from gensim.models.word2vec import Word2Vec

import sys

try:
    fname = sys.argv[1]
except:
    fname = "out.txt"

f = open(fname, 'r')

lines = f.readlines()
lines = lines[1:]

f.close()

wordVecs = {}

for line in lines:

    try:
        words = line.split()

        w = words[0]
        words = words[1:]

        vec = np.array(words, dtype = float)

        wordVecs[w] = vec
    except:
        print "Error"


# wordVecs = Word2Vec.load_word2vec_format(fname, binary=True, unicode_errors='ignore')
def getWvec(word):

    try:
        return wordVecs[word]
    except:
        return wordVecs['the']

