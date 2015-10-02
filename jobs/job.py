from componentloader import ComponentsLoader
from os.path import join
from ..models.keras_custom.utils.np_utils import to_categorical
from colorama import Fore

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

    def evaluate_dataset(self, dataset_id):

        self.loadTestMapper(dataset_id)
        return self.evaluate()

    def evaluate(self):
        
        X = self.mapper_test.X
        Y = self.mapper_test.Y

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


    def predict(self):

        X = self.mapper_test.X

        predictions = self.model.predict(X)
        self.mapper_test.unMap(self.dataset_test.X[:,0], predictions, self.mapper.cats[1])


    def gridSearch(self):

        print "Performing Grid Search"

        X = self.mapper.X
        Y = self.mapper.Y

        score = self.model.gridSearch(X,Y)
        from colorama import Fore
        print Fore.YELLOW, "\nBest Score: %.2f %%" % (score * 100)
