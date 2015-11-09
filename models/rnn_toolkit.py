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
        classes = int(p.get("class", 100))
        oldcl = int(p.get("oldclass", 0))

        flags = (p.get("flags", RNNLM_miktoolkit.defaultParams()["flags"] ))

        if oldcl == 0:
            self.flags = "-class %d -bptt %d" % (classes, bptt)
        else:
            self.flags = "-old-classes -bptt %d" % (bptt)


        self.flags = "-hidden %d %s %s" % (self.numHidden, self.flags, flags)


    @staticmethod
    def defaultParams():

        out = {
                "bptt": 4,
                "class": 100,
                "hidden_nodes": 100,
                "oldclass": 0,
                "flags" : "-rand-seed 1 -debug 2 -bptt-block 10 -direct-order 3 -direct 2 -binary"
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

        flags = (p.get("flags", RNNLM_FASTER_toolkit.defaultParams()["flags"] ))

        self.flags = "-threads %d -bptt %d" % (self.numThreads, bptt)

        self.flags = "-hidden %d %s %s" % (self.numHidden, self.flags, flags)

    @staticmethod
    def defaultParams():

        out = {
                "threads": 8,
                "bptt": 4,
                "hidden_nodes": 100,
                "flags" : "-bptt-block 10 -direct-order 3 -direct 2"
        }

        return out


