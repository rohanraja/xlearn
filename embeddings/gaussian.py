import numpy

class GaussianEmbedding():

    def __init__(self, dataset, dim=100):

        self.D = dim
        self.V = dataset.V



    def getWord2VecMatrix(self):
        
        self.WVec = 0.2 * numpy.random.uniform(-1.0, 1.0, (self.V, self.D))
        return self.WVec


