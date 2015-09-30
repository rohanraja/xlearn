import numpy as np

from basemodel import BaseModel

from sklearn import svm, cross_validation
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.neighbors import KNeighborsClassifier


class SVM_QUANT(BaseModel):

    def __init__(self, hyperParams=None):
        
        self.model = svm.SVC()


class DT_Quant(BaseModel):

    def __init__(self, hyperParams=None):
        
        self.model = DecisionTreeClassifier(random_state=4)

class RandomForest(BaseModel):

    def __init__(self, hyperParams=None):
        
        self.model = RandomForestClassifier(n_estimators=50)

class Adaboost(BaseModel):

    def __init__(self, hyperParams=None):
        
        self.model = AdaBoostClassifier(base_estimator=RandomForestClassifier(100), n_estimators=100)


class Multinomial(BaseModel):

    def __init__(self, hyperParams=None):
        
        self.model = KNeighborsClassifier()

class ExtraTrees(BaseModel):

    def __init__(self, hyperParams=None):
        
        self.model = ExtraTreesClassifier(n_estimators=200)
