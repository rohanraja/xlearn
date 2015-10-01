from os.path import join
from os import mkdir
from os import listdir

from job import Job

import json

class Project():

    baseDir = "../projects"

    def __init__(self, proname):
        
        self.projectName = proname
        self.projectDir = join(self.baseDir, proname)

        self.jinfo = self.getJobInfo()


    def getJobInfo(self):

        fname = join(self.projectDir, "jinfo.json")
        jInfo = json.load(open(fname))
        # jInfo = {
        #     
        #     "dataset_idx": 1,
        #     "mapper_idx": 1,
        #     "model_idx": 6,
        # }
        return jInfo

    def listJobs(self):

        jobs = listdir(self.projectDir)

        jobs = filter(lambda j: j.isdigit(), jobs)

        return jobs

    def getParamsInfo(self, paramsId):

        jobdir = join(self.projectDir, paramsId)
        fname = join(jobdir, "pinfo.json")
        params = json.load(open(fname))

        return params

    def getJob(self, params_name, mid = None):
        
        jobdir = join(self.projectDir, params_name)

        params= self.getParamsInfo(params_name)

        if mid :
          self.jinfo["model_idx"] = mid

        j = Job(jobdir , self.jinfo, params)

        return j


    def createParamsInfo(self, params):

        try:
            jlist = self.listJobs()
            jlist.sort(key=int)
            newPid = (int(jlist[-1]) + 1)
        except:
            newPid = 0

        jobdir = join(self.projectDir, str(newPid))
        mkdir(jobdir)
        fname = join(jobdir, "pinfo.json")

        json.dump(params, open(fname, 'w'))
        return newPid

    @staticmethod
    def list():
        projects = listdir(Project.baseDir)
        projects = filter(lambda j: j.isdigit(), projects)

        return projects

    @staticmethod
    def createModelInfo(params):
        
        try:
            jlist = Project.list()
            jlist.sort(key=int)
            newPid = (int(jlist[-1]) + 1)
        except:
            newPid = 0

        jobdir = join(Project.baseDir, str(newPid))
        mkdir(jobdir)
        fname = join(jobdir, "jinfo.json")

        json.dump(params, open(fname, 'w'))
        return newPid

