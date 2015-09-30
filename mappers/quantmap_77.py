from numpy import array
import numpy as np

from pandas import Categorical
from basemapper import BaseMapper
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from pandas import DataFrame
import re
import datetime
from sklearn import preprocessing

from colorama import Fore

class QuantMapper(BaseMapper):

    def __init__(self, dataset, removeOut = True):

        self.dataset = dataset
        self.X = self.dataset.X
        self.Y = self.dataset.Y

        self.getXY()
        
        if removeOut:
            self.remove_outliers()
            # pass
        
        self.split_train_val()


    def getXY(self):

        self.removeFeatures()
        self.Categories_with_indices()
        self.addDateDiff()

        self.binnize()

        # self.normalize()

    def binnize(self):

        self.X[:,-1] = self.binnRow(self.X[:,-1]) 
        self.X[:,-3] = self.binnRow(self.X[:,-3])
        self.X[:,-4] = self.binnRow(self.X[:,-4])

        # self.X[:,-5] = self.binnRow(self.X[:,-5], 100)
        # self.X[:,-6] = self.binnRow(self.X[:,-6], 100)



    def binnRow(self,a, numBins = 2000):
        
        bins = np.histogram(a, numBins)
        digized = np.digitize(array(a, dtype='float64'), bins[1])
        
        return array(map(lambda v: bins[1][v-1], digized)).reshape((a.shape[0],))

    def mapr(self, val):
        try:
            return int(re.findall(r'\d+',val)[0]) 
        except:
            if val == 'Y':
                return -1
            if val == 'N':
                return 1

            return 0

    def to_dint(self, dte):
        try:
            return int(datetime.datetime.strptime(dte, '%d-%b-%y').strftime("%s"))
        except:
            return 0

    def addDateDiff(self):

        iss_date = self.dataset.X[:, 8]
        exp_date = self.dataset.X[:, 12]

        iss_int = array(map(self.to_dint, iss_date), dtype=float)
        exp_int = array(map(self.to_dint, exp_date), dtype=float)
        diff = exp_int - iss_int

        diff = (diff) / 5000000.0
        iss_int /= 5000000.0
        exp_int /= 5000000.0

        for i in range(diff.shape[0]):
            if diff[i] < 0:
                diff[i] = 0


        self.X = np.append(self.X, diff.reshape((iss_int.shape[0],1)), axis=1)
        # self.X = np.append(self.X, diff.reshape((exp_int.shape[0],1)), axis=1)
        # self.X = np.append(self.X, diff.reshape((diff.shape[0],1)), axis=1)

    def remove_outliers(self):

        present = self.to_dint("29-Sep-15")
        past_thresh = self.to_dint("10-Jan-95")

        print self.X.shape

        def condition(row, i):

            c1 = self.to_dint(row[8]) < past_thresh and self.to_dint(row[12]) > present 
            c2 = self.X[i,-1] == 0 
            
            c3 = self.to_dint(row[12]) < past_thresh # and self.to_dint(row[12]) > present 
            
            return c1 or c2 or c3

        to_delete = []

        for i in range(self.X.shape[0]):
            try:
                if condition(self.dataset.X[i], i) :
                    to_delete.insert(0,i)
            except:

                to_delete.insert(0,i)

        for d in to_delete:
            self.X = np.delete(self.X, d, 0)
            self.Y = np.delete(self.Y, d)


        print self.X.shape


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

            # self.X[:,i] = c.codes
            

            self.X[:,i] = map(self.mapr, self.X[:,i])


        self.cats.append(cy)

        # self.Y = cy.codes
        self.Y = map(self.mapr, self.Y)
    
    def removeFeatures(self):
        # self.X = np.delete(self.X, 3, 1)
        self.X = np.delete(self.X, 8, 1)  # Iss Date
        # self.X = np.delete(self.X, 8, 1)  # Iss Date
        self.X = np.delete(self.X, 11, 1) # Exp Date
        self.X = np.delete(self.X, 6, 1)
        # self.X = np.delete(self.X, -3, 1) # Removed Ticker
        self.X = np.delete(self.X, 0, 1) # Removed Ticker
        # self.X = np.delete(self.X, 1, 1) # Removed Ticker


    def oneHotEncode(self):

        enc = OneHotEncoder()
        enc.fit(X)

    def normalize(self):

        self.X = preprocessing.scale(self.X)

    def unMap(self,X, Y, ycat):
        newX = []
        newY = []

        for i in range(X.shape[0]):
            # x = self.cats[0].categories[X[i]]
            # y = ycat.categories[Y[i]]
            # x = "ISIN%d" % (X[i])
            y = "Stripe %d" % (Y[i])
            # newX.append(x)
            newY.append(y)

        dataFrame = DataFrame([X, newY])

        dataFrame.transpose().to_csv("output.csv", index=False, header=["ISIN", "Risk_Stripe"])



