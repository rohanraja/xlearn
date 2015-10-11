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


    def Test_starting_training(self):

        params = { 
                "modelId": 4,
                "paramsId": 0,
                "nepochs": 465,
                "currentEpoch": 400,
                }

        # start_training(params)
        jobid = register_training_job(params)
        blocking_trainer(params, BatchCallBack(jobid))
        # print get_epoch_list(params)


    def test_evaluation(self):
        params = { 
                "modelId": 10,
                "paramsId": 0,
                "datasetId": 3,
                "nsents": 2,
                "currentEpoch": 0,
                }

        print start_evaluation(params)

    def Test_list_methods(self):

        print mappers_list({})

    
    def tesT_sentance_eval(self):

        params = { 
                "modelId": 10,
                "paramsId": 0,
                "sentance": "This is a test sentance",
                "currentEpoch": 0,
                }

        # import json
        (test_sentance(params))
        # print json.dumps(predict_next_words(params))

    def tesT_perplexicity(self):

        params = { 
                "modelId": 4,
                "paramsId": 0,
                "sentance": "This is a test sentance",
                "currentEpoch": 5,
                }


