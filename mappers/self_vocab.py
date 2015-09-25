from vocab import Vocabulary
from numpy import array
from ..models.keras_custom.preprocessing.sequence import pad_sequences

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

        self.X = pad_sequences(self.X, maxlen=100)

        Y = [0 if y==0 else 1 for y in self.dataset.Y]
        self.Y = Y #array(Y)

    def getEmbeddingsMatrix(self):

        self.Wvec = self.vocab.getWord2VecMatrix()
