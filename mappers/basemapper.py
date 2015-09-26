from sklearn import cross_validation

class BaseMapper():
    pass

    def split_train_val(self, factor = 0.5):


        X_train, X_test, y_train, y_test = cross_validation.train_test_split(
            self.X,
            self.Y, 
            test_size=factor, 
            random_state=0
        )

        self.X_train = X_train #self.X[:7000]
        self.Y_train = y_train #self.Y[:7000]
        self.X_test = X_test #self.X[7000:]
        self.Y_test = y_test #self.Y[7000:]
