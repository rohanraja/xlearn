import unittest
from colorama import Fore
from ..mappers import mappersIndex
from ..datasets import datasetsIndex
from ..models import modelsIndex
from ..models.keras_custom.preprocessing.sequence import pad_sequences

from project import Project

class TestJob_and_Project(unittest.TestCase):

    def test_running_sample_job(self):

        pname = Project.list()[0]
        p = Project(pname)
        
        jname = p.listJobs()[0]

        for i in range(9, 10): # Random Forest

            j = p.getJob(jname, i)

            j.start_training()
            # j.evaluate()
            j.predict()
            j.crossValidate()
            # j.gridSearch()
