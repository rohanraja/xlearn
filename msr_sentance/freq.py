import sys

try:
    fname = sys.argv[3]
except:
    fname = "input.txt"


f = open(fname)

txt = f.read()

words = txt.split()

freqs = {}

for w in words:

    try:
        freqs[w] += 1 
    except:
        freqs[w] = 1 

def getFreq(word):

    try:
        return freqs[word]
    except:
        return 1


