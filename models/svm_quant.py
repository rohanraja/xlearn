import numpy as np

from basemodel import BaseModel

from sklearn import svm, cross_validation
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier



class SVM_QUANT(BaseModel):

    def __init__(self, hyperParams=None):
        
        self.model = svm.SVC()


class DT_Quant(BaseModel):

    def __init__(self, hyperParams=None):
        
        self.model = DecisionTreeClassifier(random_state=10)

class RandomForest(BaseModel):

    def __init__(self, hyperParams=None):
        
        self.model = RandomForestClassifier(n_estimators=100)
class Adaboost(BaseModel):

    def __init__(self, hyperParams=None):
        
        self.model = AdaBoostClassifier(base_estimator=RandomForestClassifier(100), n_estimators=100)


