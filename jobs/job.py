from componentloader import ComponentsLoader
from os.path import join

class Job(ComponentsLoader):

    def __init__(self, pdir,  jinfo , params):

        self.jinfo = jinfo
        self.jobDir = pdir
        self.params = params

        self.weight_default_fname = "weights"

        self.loadComponents() # self.model contains model class instance
        self.load_weights()



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

        self.model.model.fit(
            X, Y, 
            batch_size=32, 
            validation_split=0.5, 
            nb_epoch=5, 
            show_accuracy=False, 
            verbose=0
        )

        self.save_weights()



    def evaluate(self):
        
        X = self.mapper.X
        Y = self.mapper.Y

        loss, accuracy = self.model.model.evaluate(
            X, Y, 
            batch_size=32, 
            show_accuracy=True, 
        )

        print accuracy * 100
