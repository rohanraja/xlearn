from textreader import TextReader

class Google_held_00(TextReader):

    def __init__(self):

        fname = "news.en.heldout-00000-of-00050"

        self.readFile(fname)
