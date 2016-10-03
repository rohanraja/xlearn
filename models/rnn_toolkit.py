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
        
        self.valid = int(p.get("valid", -1))

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

    def getPPXFromOut(self, out):

        return float(out.replace('\n','').split(':')[-1])

class RNNLM_FASTER_toolkit(BaseMikov):

    def __init__(self, hyperParams=None):

        self.params = hyperParams

        # self.execFile = "/Users/rohanraja/code/mikolov/rnnlm-0.4b/rnnlm"
        self.execFile = os.getenv('FASTRNNLM_PATH')
        p = self.params["model"]
        self.numHidden = int(p.get("hidden_nodes", 100))
        self.numThreads = int(p.get("threads", 8))
        self.valid = int(p.get("valid", -1))

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


class N_GRAM(BaseMikov):

    def __init__(self, hyperParams=None):

        self.params = hyperParams

        # self.execFile = "/Users/rohanraja/code/mikolov/rnnlm-0.4b/rnnlm"
        self.execFile = os.getenv('NGRAMCNT_PATH')
        self.execFile_test = os.getenv('NGRAM_PATH')
        p = self.params["model"]
        self.valid = int(p.get("valid", -1))

        flags = (p.get("flags", N_GRAM.defaultParams()["flags"] ))
        self.order = int(p.get("order", N_GRAM.defaultParams()["order"] ))

        self.flags = flags


    @staticmethod
    def defaultParams():

        out = {
                "flags" : "-kndiscount -interpolate -gt3min 1 -gt4min 1",
                "order" : 5,
        }
        return out

    def getEvalArgs(self, X, mod):

        progArgs = [
                
            self.execFile_test,
            "-ppl '%s'"%X,
            "-lm '%s'"%mod,
            "-order %d"%self.order,
        ]

        return progArgs
    
    def getProgArgs(self, X, val, mod):

        progArgs = [
                
            self.execFile,
            "-text '%s'"%X,
            "-lm '%s'"%mod,
            "-order %d"%self.order,
            self.flags,
        ]

        return progArgs

    def getPPXFromOut(self, out):

        return float(out.split(' ')[-3])
