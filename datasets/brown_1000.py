from selfvocab import SelfVocab

from nltk.corpus import brown

from ..models.keras_custom.preprocessing.sequence import pad_sequences
from keras.utils.np_utils import to_categorical

import numpy as np

class Brown_1000(SelfVocab):

    def __init__(self, offset=0, num=200):
        
        self.sentances = brown.sents()[offset:(offset+num)]

        self.fromSentances()

        self.X = pad_sequences(self.X)
        self.Y = pad_sequences(self.Y)

        yTmp = np.empty((200,60,1439))

        for i in range(self.Y.shape[0]):
            yTmp[i] = (to_categorical(self.Y[i], 1439))

        self.Y = (yTmp)
