import unittest
from webinterface import *
from colorama import Fore

class TestWebInterface(unittest.TestCase):

    def test_getModelInfo(self):

        params = { 
                "modelId": 0,
                "paramsId": 0,
                "pInfo":{
                    "tpino": 23
                    }
                
                }
        print Fore.GREEN, getModelInfo(params)
        print Fore.CYAN, getParamsInfo(params)
        # print Fore.RED, createParamsInfo(params)

    def test_loading_datasets(self):

        out = loadDatasets("")

        print Fore.GREEN, out
