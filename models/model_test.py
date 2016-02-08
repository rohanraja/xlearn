import unittest
from colorama import Fore
from ..mappers import mappersIndex
from ..datasets import datasetsIndex
from __init__ import modelsIndex
import numpy as np
from keras_custom.preprocessing.sequence import pad_sequences
from keras_custom.utils.np_utils import to_categorical

class TestModel(unittest.TestCase):


    def test_cgt_rnn(self):

        # DS = datasetsIndex[14]
        #
        # data = DS()
        #
        # M = mappersIndex[5]
        #
        # m = M(data)

        Model = modelsIndex[19]

        md = Model()

        md.loadWeights("test1/params_out")
        # md.train()
        # md.generateSequence()
        # md.evaluate_sentance("She ate a little amount")
        md.evaluate_sentance("The Queen said that there will be no")
        # md.evaluate_sentance("And then the Queen said to my other twin")
        md.evaluate()


    def Test_mapper_output(self):

        DS = datasetsIndex[1]

        data = DS(0)

        M = mappersIndex[1]

        m = M(data)

        Model = modelsIndex[3]

        X = m.X #pad_sequences(m.X, maxlen=100)

        print X.shape

        md = Model()

        # md.model.load_weights("weights")

        y = to_categorical(m.Y)

        loss = md.model.evaluate(X, y, batch_size=32, show_accuracy=True)
        print "Initial Loss and Accuracy: ", loss

        # md.model.fit(X, m.Y, batch_size=32, validation_split=0.5, nb_epoch=5, show_accuracy=True, verbose=1)
        # md.model.save_weights("weights", overwrite=True)
        #
        #
        yhat = md.model.predict_classes(X, batch_size=32)
        print "\n\nPredictions: ", np.min(yhat)
        print "\n\nPredictions: ", np.min(m.Y)




