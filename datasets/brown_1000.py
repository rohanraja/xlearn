from nltk.corpus import brown

class Brown_200():

    def __init__(self, offset=0, num=200):
        
        self.sentances = brown.sents()[offset:(offset+num)]

class Brown_1000():

    def __init__(self, offset=0, num=1000):
        
        self.sentances = brown.sents()[offset:(offset+num)]

class Brown_500_short_10():

    def __init__(self, offset=0, num=500):
        
        self.sentances = brown.sents() #[offset:(offset+num)]

        self.sentances = filter(lambda x: len(x) < 10, self.sentances)
        self.sentances = self.sentances[0:num]
        #
        #
        # j = 0
        # i = 0
        # length = 15
        #
        # while j<num:
        #
        #     curSent = brown.sents()[offset+i]
        #     i += 1
        #     if(len(curSent) < length):
        #         self.sentances.append(curSent)
        #         j += 1
        #         print j
        #

