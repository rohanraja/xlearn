from textreader import TextReader
from basedataset import BaseDataset

class Google_held_00(TextReader, BaseDataset):

    def __init__(self):

        # fname = "news.en-00000-of-00100"
        fname = "news.en.heldout-00000-of-00050"
        self.readFile(fname)

class Google_train_1(TextReader, BaseDataset):

    def __init__(self):

        fname = "news.en-00001-of-00100"
        # fname = "news.en.heldout-00000-of-00050"
        self.readFile(fname, True)


