from keras_custom.models import Sequential
from keras_custom.layers.core import Dense, Dropout, Activation
from keras_custom.optimizers import SGD

from keras_custom.utils.np_utils import to_categorical

# import theano
# theano.config.mode = "FAST_COMPILE"

class MLP_QUANT():

    def __init__(self, hyperParams=None):

        if hyperParams == None :
            hyperParams = {
                    'input': 15,
                    'l1_output': 4,
                    'l2_output': 4,
                    'output': 16,
            }

        p = hyperParams

        model = Sequential()

        model.add(Dense(p['input'], 5, init='uniform'))
        model.add(Activation('sigmoid'))
        model.add(Dropout(0.5))
        # model.add(Dense(24, 4, init='uniform'))
        # model.add(Activation('tanh'))
        # model.add(Dropout(0.5))
        model.add(Dense(5, p["output"]))
        model.add(Activation('softmax'))
        
        self.model = model
        self.compile()


    def compile(self):

        print "Compiling..."
        
        sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
        self.model.compile(loss='categorical_crossentropy', optimizer=sgd)
        

        # self.model.compile(loss='binary_crossentropy', optimizer='rmsprop')
        # self.model.compile(loss='binary_crossentropy', optimizer='sgd', class_mode="binary")

        print "Compiling Done"

    def train(self, X, Y, trainParams = {}):
        
        y = to_categorical(Y)
        self.model.fit(
            X, y, 
            batch_size=50, 
            # validation_split=0.2, 
            nb_epoch=10, 
            show_accuracy=True, 
            verbose=1
        )


    def evaluate(self, X, Y, trainParams = {}):
        
        y = to_categorical(Y)
        
        out = self.model.evaluate(
            X, y, 
            batch_size=32, 
            show_accuracy=True, 
        )

        return out
