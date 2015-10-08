from keras_custom.models import Sequential
from keras_custom.layers.core import Dense, Dropout, Activation
from keras_custom.layers.embeddings import Embedding
from keras_custom.layers.recurrent import LSTM
from keras_custom.layers.recurrent import SimpleRNN, SimpleDeepRNN

from basekeras import BaseKeras

import theano

theano.config.mode = "FAST_RUN"
theano.config.openmp = True

class RNN_LM_Deep(BaseKeras):

    def __init__(self, hyperParams=None):

        self.params = hyperParams

        if(self.checkSavedModel()):
            return
        
        p = self.params["model"]

        model = Sequential()
        
        embed_matrix = self.params["embedding"] 

        emb = Embedding(
                embed_matrix.shape[0], 
                embed_matrix.shape[1], 
                weights=[embed_matrix], 
                mask_zero=True,
                # learn=(self.params["learn_embedding"] == 1)
        )

        model.add(emb)

        srnn = SimpleDeepRNN(
                input_dim=embed_matrix.shape[1],
                output_dim=embed_matrix.shape[0],
                activation='softmax', 
                depth = int(p.get("depth", 3)),
                inner_activation='sigmoid',
                return_sequences=True,
        )


        print "Done"

        model.add(srnn)
        self.model = model
        self.compile()

        self.saveModel()


    def compile(self):

        print "Compiling..."
        
        # sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
        self.model.compile(loss='categorical_crossentropy', optimizer='adagrad')


        print "Compiling Done"

    @staticmethod
    def defaultParams():

        out = {
                "depth": 3
        }

        return out

class RNN_LM(BaseKeras):

    def __init__(self, hyperParams=None):

        self.params = hyperParams

        if(self.checkSavedModel()):
            return

        model = Sequential()
        
        embed_matrix = self.params["embedding"] 

        emb = Embedding(
                embed_matrix.shape[0], 
                embed_matrix.shape[1], 
                weights=[embed_matrix], 
                mask_zero=True,
                # learn=(self.params["learn_embedding"] == 1)
        )

        model.add(emb)

        srnn = SimpleRNN(
                input_dim=embed_matrix.shape[1],
                output_dim=embed_matrix.shape[0],
                activation='softmax', 
                # inner_activation='hard_sigmoid',
                return_sequences=True,
        )


        print "Done"

        model.add(srnn)

        # model.add(Activation('softmax'))

        # model.add(LSTM(embed_matrix.shape[1], 128, activation='sigmoid', inner_activation='hard_sigmoid'))
        # model.add(Dropout(0.5))
        # model.add(Dense(128, 1))
        # model.add(Activation('sigmoid'))

        self.model = model

        # import pdb; pdb.set_trace()
        self.compile()

        self.saveModel()


    def compile(self):

        print "Compiling..."
        
        # sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
        self.model.compile(loss='categorical_crossentropy', optimizer='adagrad')

        # self.model.compile(loss='binary_crossentropy', optimizer='rmsprop')
        # self.model.compile(loss='binary_crossentropy', optimizer='rmsprop', class_mode="binary")

        print "Compiling Done"
