from componentloader import ComponentsLoader

class Job(ComponentsLoader):

    def __init__(self, jinfo):

        self.jinfo = jinfo # Dict containing model, dataset, mapping information

        self.loadComponents() # self.model contains model class instance

        self.evaluate()
        self.start_training()
        self.evaluate()



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


    def evaluate(self):
        
        X = self.mapper.X
        Y = self.mapper.Y

        loss, accuracy = self.model.model.evaluate(
            X, Y, 
            batch_size=32, 
            show_accuracy=True, 
        )

        print accuracy * 100
