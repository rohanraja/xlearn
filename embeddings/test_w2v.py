import unittest
from colorama import Fore
from ..mappers import mappersIndex
from ..datasets import datasetsIndex
from w2v import *

class TestMapping(unittest.TestCase):

    def test_nepal_map(self):

        DS = datasetsIndex[8]
        data = DS()
        M = mappersIndex[3]
        m = M(data)
        

        wv = Word2Vec_3gb(m)

        embed = wv.getWord2VecMatrix()
        
        print embed.shape
        print embed
