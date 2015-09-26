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
            self.model.model.load_weights(fpath)
            print "Loaded Weights from file: %s"%fname
        except:
            print "Couldn't find saved weights"


    def save_weights(self, fname=None):
        
        if fname == None:
            fname = self.weight_default_fname

        fpath = join(self.jobDir, fname)
        self.model.model.save_weights(fpath, overwrite=True)


    def start_training(self):
        
        X = self.mapper.X
        Y = self.mapper.Y
        
        self.model.train(X,Y)

        # self.save_weights()


    def viewSample(self):
        pass

    def evaluate(self):
        
        X = self.mapper.X_test
        Y = self.mapper.Y_test

        loss, accuracy = self.model.evaluate(X,Y)

        from colorama import Fore
        print Fore.GREEN, "\nTest Set Accuracy: %.2f %%" % (accuracy * 100)

    def crossValidate(self):

        X = self.mapper.X
        Y = self.mapper.Y

        score = self.model.crossValidate(X,Y)
        from colorama import Fore
        print Fore.CYAN, "\nCrossValidateScore: %.2f %%" % (score * 100)


    def predict(self):

        X = self.mapper_test.X

        predictions = self.model.predict(X)
        self.mapper_test.unMap(X[:,0], predictions, self.mapper.cats[1])
