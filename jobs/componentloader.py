from ..models import modelsIndex
from ..datasets import datasetsIndex
from ..mappers import mappersIndex

class ComponentsLoader():
    
    def loadComponents(self):

        self.loadDataset()   # self.dataset contains the final dataset
        self.loadMapper()    
        self.loadModel()     # self.model contains the final model



    def loadMapper(self):
        M = mappersIndex.get(self.jinfo["mapper_idx"])
        self.mapper = M(self.dataset)
        self.mapper_test = M(self.dataset_test)


    def loadDataset(self):
        DS = datasetsIndex.get(self.jinfo["dataset_idx"])
        self.dataset = DS()
    
        DS_test = datasetsIndex.get(2)
        self.dataset_test = DS_test()

    def loadModel(self):

        hyperParams = self.loadHyperparams()
        # weights = self.loadWeights()

        modelClass = modelsIndex.get(self.jinfo["model_idx"])
        self.model = modelClass()

    def loadWeights(self):
        return []

    def loadHyperparams(self):
        return []


