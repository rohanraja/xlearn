import unittest
from colorama import Fore
from __init__ import datasetsIndex

class TestDatasetNepal(unittest.TestCase):

    def test_nepal(self):

        # print Fore.GREEN, "Loading Data"

        DS = datasetsIndex[8]
        ds = DS()

        print Fore.GREEN, ds.Y[100:120]


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
