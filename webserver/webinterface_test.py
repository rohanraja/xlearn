import unittest
from webinterface import *
from trainer import *
from evaluate import *
from colorama import Fore

class TestWebInterface(unittest.TestCase):

    def Test_getModelInfo(self):

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

    def Test_loading_datasets(self):

        out = loadDatasets("")

        print Fore.GREEN, out


    def test_starting_training(self):

        params = { 
                "modelId": 4,
                "paramsId": 0,
                "nepochs": 5,
                "currentEpoch": 0,
                }

        # start_training(params)
        blocking_trainer(params, BatchCallBack(""))
        # print get_epoch_list(params)


    def Test_evaluation(self):
        params = { 
                "modelId": 0,
                "paramsId": 0,
                "datasetId": 1,
                "nepochs": 5,
                "currentEpoch": 5,
                }

        print start_evaluation(params)

    def Test_list_methods(self):

        print mappers_list({})
