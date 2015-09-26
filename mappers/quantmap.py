from numpy import array

from pandas import Categorical
from basemapper import BaseMapper
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from pandas import DataFrame

class QuantMapper(BaseMapper):

    def __init__(self, dataset):

        self.dataset = dataset
        self.X = self.dataset.X
        self.Y = self.dataset.Y

        self.removeFeatures()
        self.getXY()
        self.split_train_val()

    def getXY(self):

        self.Categories_with_indices()
        self.normalize()

    def Categories_with_indices(self):

        cy = Categorical(self.Y)
        
        # print self.X[0][3]
        # print self.X[0][7]
        # print self.X[0][10]

        self.cats = []

        first = True
        for i in range(self.X.shape[1]):
            c = Categorical(self.X[:,i])

            if first:
                self.cats.append(c)
                first = False

            self.X[:,i] = c.codes
            # minmum = np.min(self.X[:,i])            
            # self.X[:,i] = self.X[:,i] - minmum + 1

        self.cats.append(cy)

        self.Y = cy.codes
    
    def removeFeatures(self):
        self.X = np.delete(self.X, 3, 1)
        self.X = np.delete(self.X, 7, 1)  # Iss Date
        self.X = np.delete(self.X, 10, 1) # Exp Date
        self.X = np.delete(self.X, 6, 1)
        self.X = np.delete(self.X, -3, 1) # Removed Ticker


    def oneHotEncode(self):

        enc = OneHotEncoder()
        enc.fit(X)

    def normalize(self):
        pass

    def unMap(self,X, Y, ycat):
        newX = []
        newY = []

        for i in range(X.shape[0]):
            x = self.cats[0].categories[X[i]]
            y = ycat.categories[Y[i]]
            newX.append(x)
            newY.append(y)

        dataFrame = DataFrame([newX, newY])

        dataFrame.transpose().to_csv("output.csv", index=False, header=["ISIN", "Risk_Stripe"])



