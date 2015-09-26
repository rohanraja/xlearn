from sklearn.cross_validation import cross_val_score
from colorama import Fore
class BaseModel():
    
    def crossValidate(self, X, Y, cv=10):
        print Fore.YELLOW, "\nCrossValidating..."
        out = cross_val_score(self.model, X, Y, cv=cv)
        return out.mean()

    def train(self, X, Y, **kwargs):

        print Fore.YELLOW, "Training..."

        self.model.fit(X, Y, **kwargs)


    def evaluate(self, X, Y, **kwargs):
        
        out = self.model.score(X,Y, **kwargs)
        return 0, out

    def predict(self, X):

        out = self.model.predict(X)
        return out
