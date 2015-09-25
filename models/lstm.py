from keras_custom.models import Sequential
from keras_custom.layers.core import Dense, Dropout, Activation
from keras_custom.layers.embeddings import Embedding
from keras_custom.layers.recurrent import LSTM

import theano

# theano.config.mode = "FAST_COMPILE"

class MLP_0():

    def __init__(self, hyperParams=None):

        if hyperParams == None :
            hyperParams = {
                    'l1_input': 100,
                    'l1_output': 64,
                    'l2_output': 64,
            }

        p = hyperParams

        model = Sequential()

        model.add(Dense(p['l1_input'], 64, init='uniform'))
        model.add(Activation('tanh'))
        model.add(Dropout(0.5))
        model.add(Dense(64, 64, init='uniform'))
        model.add(Activation('tanh'))
        model.add(Dropout(0.5))
        model.add(Dense(64, 1))
        model.add(Activation('sigmoid'))
        
        self.model = model
        self.compile()


    def compile(self):

        print "Compiling..."
        

        # self.model.compile(loss='binary_crossentropy', optimizer='rmsprop')
        self.model.compile(loss='binary_crossentropy', optimizer='rmsprop', class_mode="binary")

        print "Compiling Done"

class LSTM_0():

    def __init__(self, embed_matrix):
        model = Sequential()
        # Add a mask_zero=True to the Embedding connstructor if 0 is a left-padding value in your data

        emb = Embedding(embed_matrix.shape[0], embed_matrix.shape[1], weights=[embed_matrix], mask_zero=True)

        model.add(emb)
        model.add(LSTM(embed_matrix.shape[1], 128, activation='sigmoid', inner_activation='hard_sigmoid'))
        model.add(Dropout(0.5))
        model.add(Dense(128, 1))
        model.add(Activation('sigmoid'))

        self.model = model
        self.compile()


    def compile(self):

        print "Compiling..."
        

        # self.model.compile(loss='binary_crossentropy', optimizer='rmsprop')
        self.model.compile(loss='binary_crossentropy', optimizer='rmsprop', class_mode="binary")

        print "Compiling Done"
