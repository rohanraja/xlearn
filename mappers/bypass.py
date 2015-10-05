from basemapper import BaseMapper

class Bypass(BaseMapper):

    def __init__(self, dataset):

        self.X = dataset.X
        self.Y = dataset.Y
