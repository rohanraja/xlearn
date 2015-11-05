from keras_custom.models import Sequential
from keras_custom.layers.core import Dense, Dropout, Activation, TimeDistributedDense
from keras_custom.layers.embeddings import Embedding
from keras_custom.layers.recurrent import LSTM
from keras_custom.layers.recurrent import SimpleRNN, SimpleDeepRNN, SimpleRNN_Mikolov
from keras_custom.optimizers import SGD

from keras_custom.utils.theano_utils import floatX
from basekeras import BaseKeras

import theano

theano.config.mode = "FAST_RUN"

class RNNLM_Mikolov(BaseKeras):

    def __init__(self, hyperParams=None):

        self.params = hyperParams

        if(self.checkSavedModel()):
            return

        p = self.params["model"]
        numHidden = int(p.get("hidden_nodes", 100))
        model = Sequential()
        
        embed_matrix = self.params["embedding"].getWord2VecMatrix(numHidden) 

        emb = Embedding(
                embed_matrix.shape[0], 
                embed_matrix.shape[1], 
                weights=[embed_matrix], 
                mask_zero=True,
                # learn=(self.params["learn_embedding"] == 1)
        )

        model.add(emb)

        # import pdb; pdb.set_trace()
        print "Initialized Embeddings"
        srnn = SimpleRNN_Mikolov(
                input_dim=numHidden,
                output_dim=numHidden,
                activation='sigmoid', 
                init='uniform', 
                inner_init='uniform', 
                # inner_activation='hard_sigmoid',
                return_sequences=True,
                truncate_gradient=int(p.get("depth", 3)),
        )

        model.add(srnn)
        print "Initialized Recurrent Layer"

        denseL = TimeDistributedDense(
                input_dim=numHidden,
                output_dim=embed_matrix.shape[0],
                activation='softmax', 
                init='uniform',
                addB=False
        )

        model.add(denseL)
        print "Initialized Dense Layer"

        self.model = model
        self.compile()
        # self.saveModel()


    def compile(self):
        print "Compiling..."
        sgd = SGD(lr=1,
                decay=1e-6
                )
        self.model.compile(
                loss='categorical_crossentropy', 
                optimizer=sgd,
                # theano_mode=self.profmode
        )

        print "Compiling Done"

    @staticmethod
    def defaultParams():

        out = {
                "depth": 4,
                "hidden_nodes": 100
        }

        return out


