import numpy as np

class BaseDataset():

    def __getitem__(self, index):

        sents = np.array(self.sentances)[index].tolist()
        return sents
