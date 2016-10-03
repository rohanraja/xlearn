from xlearn.webserver.trainer import *
from xlearn.models import cgt_GRU
import numpy as np
from colorama import Fore
from os.path import join
import re
from colorama import Fore
import sys


CUP = '\x1b[1A'
ER = '\x1b[2K'
NL = CUP + ER


params = {}
params["modelId"] = sys.argv[1]
params["paramsId"] = sys.argv[2]


