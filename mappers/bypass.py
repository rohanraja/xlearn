from basemapper import BaseMapper
from selfvocab import SelfVocab

from ..models.keras_custom.preprocessing.sequence import pad_sequences
from keras.utils.np_utils import to_categorical

import numpy as np
from colorama import Fore

class SelfWordIndex(BaseMapper, SelfVocab):

    def __init__(self, dataset):
        
        self.generateVocab(dataset.sentances)
        
        print Fore.MAGENTA, "\nConverting words to indices"
        self.X, self.Y = self.getXY(dataset)
        print Fore.MAGENTA, "\nConversion Done", Fore.WHITE

    def getXY(self, dataset):

        X, Y = self.seqs_to_XY(dataset.sentances)

        X = pad_sequences(X)
        Y = pad_sequences(Y)

        yTmp = np.empty((Y.shape[0], Y.shape[1], self.V))

        for i in range(Y.shape[0]):
            yTmp[i] = (to_categorical(Y[i], self.V))

        return X, yTmp
