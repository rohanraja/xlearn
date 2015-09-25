import unittest
from colorama import Fore
from mappers import mappersIndex
from datasets import datasetsIndex

class TestMapping(unittest.TestCase):


    def test_mapper_output(self):

        DS = datasetsIndex[0]

        data = DS(0)

        M = mappersIndex[0]

        m = M(data)


        print m.Y[100:150]


