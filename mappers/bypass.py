from basemapper import BaseMapper
from selfvocab import SelfVocab

from ..models.keras_custom.preprocessing.sequence import pad_sequences
from ..models.keras_custom.utils.np_utils import to_categorical

import numpy as np
from colorama import Fore

class SelfWordIndex(BaseMapper, SelfVocab):

    def __init__(self, dataset):
        
        self.generateVocab(dataset.sentances)
        
        print Fore.MAGENTA, "\n** Mapping Dataset **"
        self.X, self.Y = self.getXY(dataset)
        print Fore.MAGENTA, "\n** Mapping Done **", Fore.WHITE

    def getXY(self, dataset):

        print Fore.MAGENTA, "Getting Word indices"
        X, Y = self.seqs_to_XY(dataset.sentances)


        print Fore.MAGENTA, "Padding Sequence"
        X = pad_sequences(X)
        Y = pad_sequences(Y)

        yTmp = np.empty((Y.shape[0], Y.shape[1], self.V))

        print Fore.MAGENTA, "Creating Categorical Ys"
        for i in range(Y.shape[0]):
            yTmp[i] = (to_categorical(Y[i], self.V))

        return X, yTmp
