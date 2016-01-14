from basedataset import BaseDataset
import numpy as np
from example_utils import fmt_row, fetch_dataset
import cgt

class Mnist_CGT(BaseDataset):

    def __init__(self):
        
        mnist = fetch_dataset("http://rll.berkeley.edu/cgt-data/mnist.npz")

        Xdata = (mnist["X"]/255.).astype(cgt.floatX)
        ydata = mnist["y"]

        np.random.seed(0)

        Xtrain = Xdata[0:60000]
        ytrain = ydata[0:60000]

        Xtest = Xdata[60000:70000]
        ytest = ydata[60000:70000]


        sortinds = np.random.permutation(60000)
        Xtrain = Xtrain[sortinds]
        ytrain = ytrain[sortinds]

        self.X = Xtrain
        self.Y = ytrain

class Mnist_CGT_Test(BaseDataset):

    def __init__(self):
        
        mnist = fetch_dataset("http://rll.berkeley.edu/cgt-data/mnist.npz")

        Xdata = (mnist["X"]/255.).astype(cgt.floatX)
        ydata = mnist["y"]

        np.random.seed(0)

        Xtrain = Xdata[0:60000]
        ytrain = ydata[0:60000]

        Xtest = Xdata[60000:70000]
        ytest = ydata[60000:70000]


        sortinds = np.random.permutation(60000)
        Xtrain = Xtrain[sortinds]
        ytrain = ytrain[sortinds]

        self.X = Xtest
        self.Y = ytest
