import pandas as pd
from numpy import array

class GS_Quant_2k15():

    def __init__(self, seed = 10):
        self.seed = seed
        self.csvfname = "../datasets/csv/Initial_Training_Data.csv"
        self.csvInit()


    def csvInit(self):
        
        xyMat = self.getXYMatrix()
        Xs = xyMat[:,:-1]
        Ys = xyMat[:,-1]

        # self.X = self.seqs_to_X(self.sentances)

        self.X = array(Xs)
        self.Y = array(Ys)


    def getXYMatrix(self):
        df = pd.read_csv(self.csvfname)


        # df1 = df[["Text", "Category"]]

        return df.as_matrix()
        # print df1.as_matrix()[0][0]

class GS_Quant_2k15_test():

    def __init__(self, seed = 10):
        self.seed = seed
        self.csvfname = "../datasets/csv/Initial_Test_Data.csv"
        self.csvInit()


    def csvInit(self):
        
        xyMat = self.getXYMatrix()
        Xs = xyMat
        Ys = xyMat[:,-1]

        # self.X = self.seqs_to_X(self.sentances)

        self.X = array(Xs)
        self.Y = array(Ys)


    def getXYMatrix(self):
        df = pd.read_csv(self.csvfname)


        # df1 = df[["Text", "Category"]]

        return df.as_matrix()
        # print df1.as_matr
