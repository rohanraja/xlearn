from os.path import join
from os import listdir

from job import Job


class Project():

    baseDir = "../projects"

    def __init__(self, proname):
        
        self.projectName = proname
        self.projectDir = join(self.baseDir, proname)

        self.jinfo = self.getJobInfo()


    def getJobInfo(self):

        fname = join(self.projectDir, "components_info")
        
        # load file
        
        jInfo = {
            
            "dataset_idx": 0,
            "mapper_idx": 0,
            "model_idx": 2,
        }
        return jInfo

    def listJobs(self):

        jobs = listdir(self.projectDir)

        return jobs


    def getJob(self, params_name):
        
        params = {}

        jobdir = join(self.projectDir, params_name)

        j = Job(jobdir , self.jinfo, params)

        return j

    @staticmethod
    def list():
        projects = listdir(Project.baseDir)
        return projects
