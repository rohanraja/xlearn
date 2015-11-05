from textreader import TextReader
from basedataset import BaseDataset

class Google_held_00(TextReader, BaseDataset):

    def __init__(self):

        # fname = "news.en-00000-of-00100"
        fname = "news.en.heldout-00000-of-00050"
        self.readFile(fname)
        self.trainFilePath = self.fpath

class Google_train_1(TextReader, BaseDataset):

    def __init__(self):

        fname = "news.en-00001-of-00100"
        # fname = "news.en.heldout-00000-of-00050"
        self.readFile(fname, True)
        self.trainFilePath = self.fpath



class Hindi_5l_train(BaseDataset):
    def __init__(self):
        self.fpath = "/home/rohanr/datasets/hindi/5lack/train.txt"
class Hindi_5l_test(BaseDataset):
    def __init__(self):
        self.fpath = "/home/rohanr/datasets/hindi/5lack/test.txt"
class Hindi_5l_val(BaseDataset):
    def __init__(self):
        self.fpath = "/home/rohanr/datasets/hindi/5lack/val.txt"
