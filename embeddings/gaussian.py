import numpy

class GaussianEmbedding():

    def __init__(self, dataset, dim=100):

        self.D = dim
        self.V = dataset.V



    def getWord2VecMatrix(self, num=0):

        if num == 0:
            num = self.D
        
        self.WVec = 0.2 * numpy.random.uniform(-1.0, 1.0, (self.V, num))
        return self.WVec


