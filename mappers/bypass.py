from basemapper import BaseMapper
from selfvocab import SelfVocab

from ..models.keras_custom.preprocessing.sequence import pad_sequences
from ..models.keras_custom.utils.np_utils import to_categorical

import numpy as np
from colorama import Fore
from lazyarray import LazyArray

class SelfWordIndex(BaseMapper, SelfVocab):

    def __init__(self, dataset):
        
        self.generateVocab(dataset.sentances)
        
        # print Fore.MAGENTA, "\n** Mapping Dataset **\n"
        self.X, self.Y = self.getXY(dataset)
        # print Fore.MAGENTA, "\n** Mapping Done **\n", Fore.WHITE

    def getXY(self, dataset):

        # X, Y = self.processSentances(dataset.sentances)
        X = LazyArray(dataset, self.processSentances, True)
        Y = LazyArray(dataset, self.processSentances, False)
 

        return X, Y


    def processSentances(self, sents):

        # print Fore.MAGENTA, "Getting Word indices"
        X, Y = self.seqs_to_XY(sents)


        # print Fore.MAGENTA, "Padding Sequence"
        X = pad_sequences(X)
        Y = pad_sequences(Y)

        yTmp = np.empty((Y.shape[0], Y.shape[1], self.V))

        # print Fore.MAGENTA, "Creating Categorical Ys"
        for i in range(Y.shape[0]):
            yTmp[i] = (to_categorical(Y[i], self.V))

        return X, yTmp
