from os.path import join
import cPickle
import sys
sys.setrecursionlimit(99999)
from keras_custom.layers.embeddings import Embedding
from keras_custom.utils.theano_utils import floatX

import theano
theano.config.reoptimize_unpickled_function = False

class BaseKeras():

    def train(self, X, Y, nepochs, callbacks):

        print "Training Keras Model"
        # print self.params
        # print X.shape

        # ans = self.model.predict(X)
        # print ans.shape
        # print ans[0].shape
        # print Y.shape

        self.model.fit(
                X, 
                Y, 
                nb_epoch=nepochs, 
                batch_size= int(self.params["optimizer"]["batch_size"]),
                show_accuracy=True,
                # verbose=0,
                # validation_split=0.9,
                callbacks=callbacks
        )

    def evaluate(self, X, Y):
        
        print "Evaluating Keras Model"
        out = self.model.evaluate(
            X, Y, 
            batch_size=1, 
            show_accuracy=True, 
        )

        return out

    def predict(self, X):
        
        # print "Predicting Keras Model"
        out = self.model.predict(
            X,  
            batch_size=int(self.params["optimizer"]["batch_size"]),
        )

        return out

    def saveWeights(self, fpath):

        print "Saving KERAS Weights in %s" % fpath

        self.model.save_weights(fpath, overwrite=True)


    def loadWeights(self, fpath):

        print "Loading KERAS Weights in %s" % fpath
        self.model.load_weights(fpath)

    def checkSavedModel(self):

        try:
            fpath = join(self.params["jobDir"], "model.save")
            print "Trying Loading KERAS MODEL in %s" % fpath
            f = file(fpath, 'rb')
            self.model = cPickle.load(f)
            f.close()
            print "Sucessfully Loaded compiled model from file"
            return True
        except Exception, e:
            print e
            return False

    def saveModel(self):

        fpath = join(self.params["jobDir"], "model.save")
        print "Saving KERAS MODEL in %s" % fpath

        f = file(fpath, 'wb')
        cPickle.dump(self.model, f, protocol=cPickle.HIGHEST_PROTOCOL)
        f.close()
        print "Model Saved"


    def setEmbeddingWeights(self, embed_matrix):

        # emb = Embedding(
        #         embed_matrix.shape[0], 
        #         embed_matrix.shape[1], 
        #         weights=[embed_matrix], 
        #         mask_zero=True,
        #         # learn=(self.params["learn_embedding"] == 1)
        # )
        #
        # self.model.layers[0] = emb

        self.model.layers[0].W.set_value(floatX(embed_matrix))
        # self.model.layers[0].set_weights([embed_matrix])
        print "Changed embed layer weights!"

        # self.compile()

    def getSize(self):

        ans = 0.0

        for W in self.model.params :
            ans += W.get_value().nbytes

        return ans/pow(2,20)
