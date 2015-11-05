from basetoolkit import BaseMikov
import os

class RNNLM_miktoolkit(BaseMikov):

    def __init__(self, hyperParams=None):

        self.params = hyperParams

        # self.execFile = "/Users/rohanraja/code/mikolov/rnnlm-0.4b/rnnlm"
        self.execFile = os.getenv('RNNLM_PATH')
        p = self.params["model"]
        self.numHidden = int(p.get("hidden_nodes", 100))
        bptt = int(p.get("bptt", 8))
        self.flags = "-rand-seed 1 -debug 2 -class 100 -bptt %d -bptt-block 10 -direct-order 3 -direct 2 -binary" % bptt



    @staticmethod
    def defaultParams():

        out = {
                "depth": 4,
                "bptt": 4,
                "hidden_nodes": 100
        }

        return out

class RNNLM_FASTER_toolkit(BaseMikov):

    def __init__(self, hyperParams=None):

        self.params = hyperParams

        # self.execFile = "/Users/rohanraja/code/mikolov/rnnlm-0.4b/rnnlm"
        self.execFile = os.getenv('FASTRNNLM_PATH')
        p = self.params["model"]
        self.numHidden = int(p.get("hidden_nodes", 100))
        self.numThreads = int(p.get("threads", 8))

        bptt = int(p.get("bptt", 8))
        self.flags = "-threads %d -bptt %d -bptt-block 10 -direct-order 3 -direct 2" % (self.numThreads, bptt)


    @staticmethod
    def defaultParams():

        out = {
                "depth": 4,
                "threads": 8,
                "bptt": 4,
                "hidden_nodes": 100
        }

        return out


