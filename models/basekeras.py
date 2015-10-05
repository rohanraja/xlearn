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
            batch_size=32, 
            show_accuracy=True, 
        )

        return out

    def saveWeights(self, fpath):

        print "Saving KERAS Weights in %s" % fpath

        self.model.save_weights(fpath, overwrite=True)


    def loadWeights(self, fpath):

        print "Loading KERAS Weights in %s" % fpath
        self.model.load_weights(fpath)
