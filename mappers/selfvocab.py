from numpy import array

class SelfVocab():

    def generateVocab(self, sentances):
        """
        Create self.vocab from self.sentances
        """
    
        self.brown = True
        self.vocab = set(["UNKNOWN","<s>"])
        for s in sentances :
            for w in s :
                self.vocab.add(w.lower())

        self.vocab.add("</s>")

        self.V = len(self.vocab)        
        self.numToWord = dict(enumerate(self.vocab))
        self.wordToNum = dict((v,k) for k,v in self.numToWord.iteritems())


    def seqs_to_XY(self, sentances):

        seqs_with_idx = self.docs_to_indices(sentances)

        X, Y = zip(*[self.offset_seq(s) for s in seqs_with_idx])
        return array(X, dtype=object), array(Y, dtype=object)

    def seq_to_indices(self, words):

        return array([self.wordToNum.get(w.lower(), 0) for w in words])

    def docs_to_indices(self, docs=None):
        # docs = [pad_sequence(seq, left=1, right=1) for seq in docs]
        if docs == None:
            docs = self.sentances
        ret = []
        for seq in docs:
            # words = [canonicalize_word(wt[0], word_to_num) for wt in seq]
            try:
                words = seq.split(' ')
            except:
                words = seq

            words.append("</s>")
            words.insert(0,"<s>")
            # if len(words) < 4:
            #     continue
            ret.append(self.seq_to_indices(words))

        # return as numpy array for fancier slicing
        return array(ret, dtype=object)

    def offset_seq(self, seq):
        return seq[:-1], seq[1:]


    def idx_to_sequence(self, seq):

        out = [self.numToWord.get(s, "_") for s in seq]
        return out

