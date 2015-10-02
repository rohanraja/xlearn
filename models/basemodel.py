from sklearn.cross_validation import cross_val_score
from colorama import Fore
from sklearn.externals import joblib
from sklearn.grid_search import GridSearchCV


class BaseModel():
    
    def crossValidate(self, X, Y, cv=10):
        print Fore.YELLOW, "\nCrossValidating..."
        out = cross_val_score(self.model, X, Y, cv=cv)
        return out.mean()

    def train(self, X, Y, *args, **kwargs):

        print Fore.YELLOW, "Training..."

        self.model.fit(X, Y)


    def evaluate(self, X, Y, **kwargs):
        
        out = self.model.score(X,Y, **kwargs)
        return 0, out

    def predict(self, X):

        out = self.model.predict(X)
        return out

    def save(self, fpath):
        joblib.dump(self.model, fpath) 

    def load(self, fpath):
        self.model = joblib.load(fpath) 


    def gridSearch(self, X, Y):
        
        Cs = range(50, 450, 50)

        clf = GridSearchCV(
                estimator=self.model, 
                param_grid=dict(n_estimators=Cs),
                n_jobs=-1
        )

        clf.fit(X,Y)

        print clf.best_params_
        print clf.best_estimator_
        
        return clf.best_score_
