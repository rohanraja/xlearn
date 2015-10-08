from componentloader import ComponentsLoader
from os.path import join
from ..models.keras_custom.utils.np_utils import to_categorical
from colorama import Fore
import numpy as np
from random import randint

# ayandas84@gmail.com

class Job(ComponentsLoader):

    def __init__(self, pdir,  jinfo , params):

        self.jinfo = jinfo
        self.jobDir = pdir
        self.params = params

        self.weight_default_fname = "weights"

        self.loadComponents() # self.model contains model class instance
        # self.load_weights()
        
        print Fore.MAGENTA, "\nModel: %s\n"%(self.model.__class__.__name__)




    def load_weights(self, fname=None):
        
        if fname == None:
            fname = self.weight_default_fname

        fpath = join(self.jobDir, fname)
        try:
            # self.model.model.load_weights(fpath)
            self.model.loadWeights(fpath)
            
            print "Loaded Weights from file: %s"%fpath
        except:
            print "Couldn't find saved weights"


    def save_weights(self, fname=None):
        
        if fname == None:
            fname = self.weight_default_fname

        fpath = join(self.jobDir, fname)
        # self.save(fpath)
        # self.model.model.save_weights(fpath, overwrite=True)
        self.model.saveWeights(fpath)


    def start_training(self, nepochs=5, callbacks=None):
        
        X = self.mapper.X
        Y = self.mapper.Y
        
        self.model.train(X,Y, nepochs, callbacks)

        # self.save_weights()


    def viewSample(self):
        pass

    def evaluate_dataset(self, dataset_id, num=20):

        self.loadTestMapper(dataset_id, num)

        ppxConcat = self.perplexicity_sequence(self.X_test.ravel())

        print Fore.GREEN, "\nPerplexicity %.2f\n" % ppxConcat
        ppxs = []

        for i in range(self.X_test.shape[0]):
            ppx = self.perplexicity_sequence(self.X_test[i])
            print ppx
            ppxs.append(ppx)

        ppxs = np.array(ppxs)

            
        return ppxs.mean(), ppxs.std(), ppxConcat

        # return self.evaluate(self.X_test, self.Y_test)

    def evaluate_sentance(self, sentance):
        class dummy():
            pass
        ds = dummy()
        ds.sentances = [sentance.split(" ")]
        X, Y = self.mapper.getXY(ds)
        X = np.delete(X,0,1)
        return self.perplexicity_sequence(X[0])

    def perplexicity_sequence(self, x):
        """
        x - sequence of word ids
        """
        X = x[:-1]
        y = x[1:]
        predictions = self.model.predict(np.array([X]))
        
        totalProb = 0.0

        for i, wordPreds in enumerate(predictions[0]):
            pWord = wordPreds[y[i]]
            totalProb -= np.log2(pWord)

        meanProb = totalProb / float(len(X))
        
        perplexicity = np.exp2(meanProb)

        return perplexicity
 

    def predict_sentance(self, sentance):

        class dummy():
            pass
        ds = dummy()
        ds.sentances = [sentance.split(" ")]
        X, Y = self.mapper.getXY(ds)
        X = np.delete(X,0,1)


        predictions = self.model.predict(X)

        outMap = []
        # import pdb; pdb.set_trace()
        
        N = 10 # Top N Predictions
        X_words = self.mapper.idx_to_sequence(X[0])

        for i, val in enumerate(X_words):

            wordPreds = predictions[0][i]
            topNWords = wordPreds.argsort()[-10:]
            topNWords = topNWords[::-1]
            topNProbabs = wordPreds[topNWords]

            topNWords = self.mapper.idx_to_sequence(topNWords)

            omap = {}
            omap[val] = zip(topNWords, topNProbabs)
            outMap.append(omap)
        
        return outMap

    def generate_sentance(self, start="<s>", limit=30):

        sentance = start
        
        for i in range(limit):

            nextWord = self.predict_sentance(sentance)[-1]
            for k in nextWord:
                nWord, prob = nextWord[k][randint(0,5)]
            
            sentance = "%s %s"%(sentance,nWord)
            print Fore.CYAN, nWord
            
        print Fore.MAGENTA, sentance
        return sentance


    def evaluate(self, X, Y):

        loss, accuracy = self.model.evaluate(X,Y)

        from colorama import Fore
        print Fore.GREEN, "\nTest Set Accuracy: %.2f %%" % (accuracy * 100)
        print Fore.CYAN, "\nTest Set Loss: %.4f %%" % (loss)

        return (loss, accuracy)

    def crossValidate(self):

        X = self.mapper.X
        Y = self.mapper.Y

        score = self.model.crossValidate(X,Y)
        from colorama import Fore
        print Fore.CYAN, "\nCrossValidateScore: %.2f %%" % (score * 100)


    def predict(self, X):

        # X = self.mapper_test.X

        predictions = self.model.predict(X)
        # self.mapper_test.unMap(self.dataset_test.X[:,0], predictions, self.mapper.cats[1])


    def gridSearch(self):

        print "Performing Grid Search"

        X = self.mapper.X
        Y = self.mapper.Y

        score = self.model.gridSearch(X,Y)
        from colorama import Fore
        print Fore.YELLOW, "\nBest Score: %.2f %%" % (score * 100)
