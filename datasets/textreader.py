from os.path import join

class TextReader():

    baseDir = "../datasets/googlebench"
    baseTrainDir = "/home/rohanr/datasets/training-monolingual.tokenized.shuffled"

    def readFile(self, fname, train=False):
        if train:
            fpath = join(self.baseTrainDir, fname)
        else:
            fpath = join(self.baseDir, fname)

        self.fpath = fpath

    def sentances(self):
        f = open(self.fpath, 'r')
        
        self.sentances = f.read().splitlines() #.readlines()
        self.sentances = map(lambda s: s.split(' '), self.sentances)

        f.close()

        return self.sentances
