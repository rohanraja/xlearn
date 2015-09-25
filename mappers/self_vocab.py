from vocab import Vocabulary
from numpy import array

class SelfVocab():

    def __init__(self, dataset):

        self.dataset = dataset

        self.vocab = Vocabulary()
        self.vocab.fromSentances(dataset.X)
        
        self.getXY()
        self.getEmbeddingsMatrix()


    def getXY(self):

        seqs_with_idx = self.vocab.docs_to_indices()
        self.X = array(seqs_with_idx, dtype=object)
        self.X = seqs_with_idx

        Y = [0 if y==0 else 1 for y in self.dataset.Y]
        self.Y = Y #array(Y)

    def getEmbeddingsMatrix(self):

        self.Wvec = self.vocab.getWord2VecMatrix()
