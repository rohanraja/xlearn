vsk = Word2VecKeras(gensim.models.word2vec.LineSentence('test.txt'),iter=100)
print( vsk.most_similar('the', topn=5))

from nltk.corpus import brown
brk = Word2VecKeras(brown.sents(),iter=10)
print( brk.most_similar('the', topn=5))
