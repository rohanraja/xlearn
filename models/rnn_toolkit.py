from basetoolkit import BaseMikov
import os

class RNNLM_miktoolkit(BaseMikov):

    def __init__(self, hyperParams=None):

        self.params = hyperParams

        # self.execFile = "/Users/rohanraja/code/mikolov/rnnlm-0.4b/rnnlm"
        self.execFile = os.getenv('RNNLM_PATH')
        p = self.params["model"]
        self.numHidden = int(p.get("hidden_nodes", 100))


    @staticmethod
    def defaultParams():

        out = {
                "depth": 4,
                "hidden_nodes": 100
        }

        return out


