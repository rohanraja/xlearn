import unittest
from colorama import Fore
from __init__ import datasetsIndex

class TestDatasetNepal(unittest.TestCase):


    def test_loading_dataset(self):

        print Fore.RED, "Loading Data"

        DS = datasetsIndex[0]

        ds = DS(0)

        print ds.X, ds.Y

        
