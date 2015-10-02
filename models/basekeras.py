class BaseKeras():

    def train(self, X, Y, nepochs, callbacks):

        print "Training Keras Model"
        # print self.params
        # print X.shape

        self.model.fit(
                X, 
                Y, 
                nb_epoch=nepochs, 
                batch_size=self.params["optimizer"]["batch_size"],
                # show_accuracy=True,
                verbose=0,
                callbacks=callbacks
        )

