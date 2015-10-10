from nltk.corpus import brown
from basedataset import BaseDataset

class Brown_200(BaseDataset):

    def __init__(self, offset=0, num=200):
        
        self.sentances = brown.sents()[offset:(offset+num)]

class Brown_1000(BaseDataset):

    def __init__(self, offset=0, num=1000):
        
        self.sentances = brown.sents()[offset:(offset+num)]

class Brown_500_short_10(BaseDataset):

    def __init__(self, offset=0, num=500):
        
        self.sentances = brown.sents() #[offset:(offset+num)]

        self.sentances = filter(lambda x: len(x) < 10, self.sentances)
        self.sentances = self.sentances[0:num]
