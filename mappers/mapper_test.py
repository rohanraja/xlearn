import unittest
from colorama import Fore
from __init__ import mappersIndex
from ..datasets import datasetsIndex

class TestMapping(unittest.TestCase):

    def test_GS_Map1(self):

        DS = datasetsIndex[3]
        data = DS(0, 20)
        M = mappersIndex[2]
        m = M(data)

        print Fore.YELLOW, "\n", m.X[range(10)].shape
        print Fore.YELLOW, "\n", m.Y[range(10)].shape
        # print Fore.GREEN, "\n", m.Y.shape
        # print Fore.CYAN, "\n", m.getstats()
        # print Fore.YELLOW, "\n", data.X[2][8]

    def tesT_mapper_output(self):

        DS = datasetsIndex[0]
        data = DS(0)
        M = mappersIndex[0]
        m = M(data)

        print Fore.GREEN, "\n", m.Y[10:15]


