import pandas as pd
from numpy import array
from basedataset import BaseDataset

class Tweet_Gurdaspur(BaseDataset):

    def __init__(self, seed = 10):
        self.seed = seed
        self.csvfname = "../datasets/csv/gurudaspur_english_labelled.csv"

        self.csvInit()


    def csvInit(self):
        
        xyMat = self.getXYMatrix()
        Xs = xyMat[:,0]
        Ys = xyMat[:,1]

        # self.X = self.seqs_to_X(self.sentances)

        self.X = array(Xs, dtype=object)
        self.sentances = self.X
        self.Y = array(Ys, dtype=int)


    def getXYMatrix(self):
        df = pd.read_csv(self.csvfname)

        df1 = df[["Text", "Category"]]

        return df1.as_matrix()
        # print df1.as_matrix()[0][0]

class Tweet_Nepal(BaseDataset):

    def __init__(self, seed = 10):
        self.seed = seed
        self.csvfname = "../datasets/csv/nepal_english_labelled.csv"

        self.csvInit()


    def csvInit(self):
        
        xyMat = self.getXYMatrix()
        Xs = xyMat[:,0]
        Ys = xyMat[:,1]

        # self.X = self.seqs_to_X(self.sentances)

        self.X = array(Xs, dtype=object)
        self.sentances = self.X
        self.Y = array(Ys, dtype=int)


    def getXYMatrix(self):
        df = pd.read_csv(self.csvfname)

        df1 = df[["Text", "Category"]]

        return df1.as_matrix()
        # print df1.as_matrix()[0][0]

