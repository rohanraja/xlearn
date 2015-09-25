from numpy import array
import numpy

class Vocabulary():

    def __init__(self):

        self.numToWord = {}
        self.wordToNum = {}
    
    def fromDict(self, w2numdict={}):

        self.numToWord = w2numdict
        self.wordToNum = dict((v,k) for k,v in self.numToWord.iteritems())

        self.V = len(self.numToWord)
        self.D = 100
        

    def fromSentances(self, sentances):
        
        self.sentances = sentances
        words = set(["UNK", "<s>", "</s>"])
        for s in sentances:
            for w in s.split(' '):
                for w2 in w.split('.'):
                    words.add(w2)


        self.V = len(words)
        self.D = 100
        self.numToWord = dict(enumerate(words))
        self.wordToNum = dict((v,k) for k,v in self.numToWord.iteritems())

    def getWord2VecMatrix(self):
        
        self.WVec = 0.2 * numpy.random.uniform(-1.0, 1.0, (self.V, self.D))
        return self.WVec

    def seq_to_indices(self, words):

        return numpy.array([self.wordToNum.get(w.lower(), 0) for w in words])

    def idx_to_sentance(self, seq):

        out = [self.numToWord.get(s, "_") for s in seq]
        return ' '.join(out)


    def docs_to_indices(self, docs=None):
        # docs = [pad_sequence(seq, left=1, right=1) for seq in docs]
        if docs == None:
            docs = self.sentances
        ret = []
        for seq in docs:
            # words = [canonicalize_word(wt[0], word_to_num) for wt in seq]
            try:
                words = seq.split(' ')
            except:
                words = seq

            words.append("</s>")
            words.insert(0,"<s>")
            if len(words) < 3:
                continue
            ret.append(self.seq_to_indices(words))

        # return as numpy array for fancier slicing
        return array(ret, dtype=object)

