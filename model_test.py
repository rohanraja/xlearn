import unittest
from colorama import Fore
from mappers import mappersIndex
from datasets import datasetsIndex
from models import modelsIndex
from models.keras_custom.preprocessing.sequence import pad_sequences

class TestModel(unittest.TestCase):


    def test_mapper_output(self):

        DS = datasetsIndex[0]

        data = DS(0)

        M = mappersIndex[0]

        m = M(data)

        Model = modelsIndex[2]

        X = pad_sequences(m.X, maxlen=100)
        print X.shape
        md = Model(embed_matrix = m.Wvec)

        md.model.load_weights("weights")

        loss = md.model.evaluate(X[:100], m.Y[:100], batch_size=32, show_accuracy=True)
        print "Initial Loss and Accuracy: ", loss

        md.model.fit(X, m.Y, batch_size=32, validation_split=0.5, nb_epoch=5, show_accuracy=True, verbose=1)
        md.model.save_weights("weights", overwrite=True)
        

        yhat = md.model.predict_classes(X, batch_size=32)
        print "\n\nPredictions: ", yhat




