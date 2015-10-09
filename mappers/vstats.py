class VocabStats():

    def getstats(self):
        
        out = {

                "Vocabulary Size": self.V,
                "Number of tokens": self.getNumTokens()

        }
        return out 

    def getNumTokens(self):

        AllSents = map(len, self.sentances)
        return sum(AllSents)
