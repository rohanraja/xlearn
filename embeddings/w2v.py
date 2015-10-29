import numpy
import word2vec as wv


class BaseGoogleW2v():

    def getWord2VecMatrix(self):

        print "Loading Word2Vec Model Binary"

        self.model = wv.load(self.binName)
        self.D = self.model.vectors.shape[1]
        self.V = self.dataset.V

        self.WVec = numpy.zeros((self.V, self.D))
        
        print "Copying Vectors from Word2Vec"
        for i in xrange(self.V):
            w = self.dataset.numToWord[i]
            try:
                self.WVec[i] = self.model[w]
            except:
                print "\nWord %s not found" % w
                pass

        print "Word2Vec Matix Generation Completed"
        return self.WVec



class Word2Vec_3gb(BaseGoogleW2v):

    def __init__(self, dataset, dim=100):

        self.dataset = dataset
        self.binName = "/Users/rohanraja/code/word2vec/GoogleNews-vectors-negative300.bin"

class Word2Vec_small(BaseGoogleW2v):

    def __init__(self, dataset, dim=100):

        self.dataset = dataset
        self.binName = "/Users/rohanraja/code/word2vec/vectors.bin"
        
