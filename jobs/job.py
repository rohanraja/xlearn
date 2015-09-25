from ..models import modelsIndex
from ..datasets import datasetsIndex
from ..mapper import mappersIndex

class Job():

    def __init__(jinfo):

        self.jobInfo = jinfo # Dict containing model, dataset, mapping information

        self.loadModel()     # self.model contains the final model
        self.loadDataset()   # self.dataset contains the final dataset
        self.loadMapper()    
        

    def loadMapper(self):
        self.mapper = mappersIndex.get(self.jinfo["mapper_idx"])


    def loadDataset(self):
        self.dataset = datasetsIndex.get(self.jinfo["dataset_idx"])
        
    

    def loadModel(self):

        hyperParams = self.loadHyperparams()
        weights = self.loadWeights()

        modelClass = modelsIndex.get(self.jinfo["model_idx"])
        self.model = modelClass(hyperParams, weights)

    def loadWeights(self):
        return []

    def loadHyperparams(self):
        return []
