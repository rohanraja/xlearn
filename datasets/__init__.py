from tweet_nepal import *
from gsquant import *
from brown_1000 import *
from google_bench import *
from mnist import *
import json

datasetsIndex = {

    0 : Tweet_Nepal,
    1 : GS_Quant_2k15,
    2 : GS_Quant_2k15_test,
    3 : Brown_200,
    4 : Brown_1000,
    5 : Brown_500_short_10,
    6 : Google_held_00,
    7 : Google_train_1,
    8 : Tweet_Gurdaspur,
    9 : Hindi_5l_train,
    10 : Hindi_5l_test,
    11 : Hindi_5l_val,
    12 : Mnist_CGT,
    13 : Mnist_CGT_Test,
}

from basedataset import BaseDataset

def getDataset(fname):

  class f(BaseDataset):
    def __init__(self):
      self.fpath = fname

  # f.__name__ = fname.replace('/','-').replace('.','_')
  print fname
  f.__name__ = str(fname)

  return f

otherFname = "../datasets/googlebench/others.json"

def getOtherFiles():
  try:
    out = json.load(open(otherFname, 'r'))
  except:
    out = {}
  return out

def addOtherFiles(fileName):

  out = getOtherFiles()
  cnt = len(datasetsIndex) + 1
  out[cnt] = fileName

  datasetsIndex[cnt] = getDataset(fileName)
  json.dump(out, open(otherFname, 'w'))

otherFiles = getOtherFiles()



for cidx in otherFiles:

  datasetsIndex[int(cidx)] = getDataset(otherFiles[cidx])

