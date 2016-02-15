from xlearn.webserver.trainer import *
from xlearn.models import cgt_GRU
import numpy as np
from colorama import Fore
from os.path import join
import re
from colorama import Fore
import sys

cgt_GRU.config["isTraining"] = True
cgt_GRU.config["isLoss"] = True
cgt_GRU.IS_SAVING = False
cgt_GRU.IS_TIMING = True
cgt_GRU.bend = "python"

CUP = '\x1b[1A'
ER = '\x1b[2K'
NL = CUP + ER


params = {}
params["modelId"] = sys.argv[1]
params["paramsId"] = sys.argv[2]


questions = {}

job = getJob(params)

job.model.loadWeights()

job.model.train()


