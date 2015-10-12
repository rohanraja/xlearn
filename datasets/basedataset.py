import numpy as np

class BaseDataset():

    def __getitem__(self, index):

        sents = np.array(self.sentances)[index].tolist()
        return sents


    def search(self, phrase):

        results = []
        phrase = phrase.lower()

        for s in self.sentances :
            sent = ' '.join(map(lambda w: w.lower(),s))
            if phrase in sent:
                results.append(sent.replace(phrase, "<b>%s</b>"%phrase))




        return results[:20]
