from ..models import modelsIndex
from ..datasets import datasetsIndex
from ..mappers import mappersIndex
from ..embeddings import embeddingsIndex

class ComponentsLoader():
    
    def loadComponents(self):

        self.loadDataset()   # self.dataset contains the final dataset
        self.loadMapper()    
        self.loadEmbedding()     
        self.loadModel()     # self.model contains the final model



    def loadMapper(self):
        M = mappersIndex.get(self.jinfo["mapper_id"])
        self.mapper = M(self.dataset)
        # self.mapper_test = M(self.dataset_test, False)

    def loadTestMapper(self, dataset_id):

        DS = datasetsIndex.get(dataset_id)
        dataset_test = DS()
        M = mappersIndex.get(self.jinfo["mapper_id"])
        self.mapper_test = M(dataset_test)

    def loadDataset(self):
        DS = datasetsIndex.get(self.jinfo["dataset_id"])
        self.dataset = DS()
    
        # DS_test = datasetsIndex.get(2)
        # self.dataset_test = DS_test()

    def loadModel(self):

        modelClass = modelsIndex.get(self.jinfo["model_id"])
        self.model = modelClass(self.params)

    def loadEmbedding(self):

        try:
            E = embeddingsIndex.get(self.jinfo["embedding_id"])
            self.embedding = E(self.dataset)
            self.params["embedding"] = self.embedding.getWord2VecMatrix()
        except:
            pass

    def loadWeights(self):
        return []

    def loadHyperparams(self):
        return []


