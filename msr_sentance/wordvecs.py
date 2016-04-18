import numpy as np

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


def getWvec(word):

    try:
        return wordVecs[word]
    except:
        return wordVecs['a']

