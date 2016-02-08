import unittest
from colorama import Fore
from __init__ import datasetsIndex
from seqloader import Loader
import cgt
import numpy as np

def ind2onehot_cgt(inds, n_cls):
    out = cgt.zeros(( inds.shape[0] , inds.shape[1] , n_cls))
    slinds = cgt.arange(inds.shape[0]*inds.shape[1] ) * n_cls + inds.flatten()
    ee = cgt.ones(slinds.shape)
    d = cgt.inc_subtensor(out.flatten(), slinds , ee)
    o = d.reshape(( inds.shape[0] , inds.shape[1] , n_cls))
    f = cgt.function([], [o])

    print f()[0].shape
    return d

class TestDatasetNepal(unittest.TestCase):

    def tEst_cgt_ind2one(self):
        print "Test"

        inpMat = cgt.shared( np.array([[3,2,5] ,[4,1,0]] , dtype = "i") )
        # inpMat = cgt.shared(np.ones((2,3)))
        size_vocal = 10# cgt.shared(10)

        return ind2onehot_cgt(inpMat, size_vocal)

        # a = cgt.shared(np.zeros((3,3,1)))
        a = cgt.zeros(((3,3,1)))
        b = a

        c = b.flatten()
        # e = cgt.shared(np.array([0.0, 5.0]))
        e = cgt.shared(np.arange(2))

        # ee = cgt.shared(np.array([1.0, 5.0]))
        ee = cgt.ones(e.shape)

        d = cgt.inc_subtensor(c, e , ee)

        f = cgt.function([], [d])

        print f()

    def test_rnn_loader(self):
        
        l = Loader("../datasets/sherlok" , 64, 6,(1,0,0), True)
        x,y = l.train_batches_iter().next()

        # print Fore.GREEN, l.char2ind
        print Fore.YELLOW, l.size_vocab
        print Fore.YELLOW, x.shape

    def Test_dataset(self):

        # print Fore.GREEN, "Loading Data"

        DS = datasetsIndex[14]
        ds = DS()

        print Fore.GREEN, ds.X.test_batches_iter().next()


    def Test_brown(self):

        # print Fore.GREEN, "Loading Data"

        DS = datasetsIndex[6]
        ds = DS()

        print Fore.GREEN, ds.search("the most")

    def Test_quant(self):

        # print Fore.GREEN, "Loading Data"

        DS = datasetsIndex[2]
        ds = DS()

        print Fore.GREEN, ds.X[0]
        print Fore.YELLOW, ds.Y[100]

    def tesT_loading_dataset(self):

        print Fore.RED, "Loading Data"
        DS = datasetsIndex[0]
        ds = DS(0)

        print ds.X, ds.Y
