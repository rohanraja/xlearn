import numpy as np

class LazyArray():

    def __init__(self, dataset, processor, isX = True):
        self.dataset = dataset
        self.processor = processor
        self.isX = isX
        self.shape = (len(dataset.sentances), 1)


    def __len__(self):
        return len(self.dataset.sentances)

    def __getitem__(self, index):

        retSingle = False

        # if type(index) != list:
        if not hasattr(index, "__len__"):
            index = [index]
            retSingle = True

        sents = self.dataset[index]
        X, Y = self.processor(sents)

        if self.isX :
            out = X
        else:
            out = Y


        if retSingle:
            return out[0]
        else:
            return out

    def ravel(self):

        X, Y = self.processor(self.dataset.sentances)
        return X.ravel()

    

