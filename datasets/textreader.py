from os.path import join

class TextReader():

    baseDir = "../datasets/googlebench"

    def readFile(self, fname):
        fpath = join(self.baseDir, fname)

        f = open(fpath, 'r')
        
        self.sentances = f.read().splitlines() #.readlines()
        self.sentances = map(lambda s: s.split(' '), self.sentances)

        f.close()
