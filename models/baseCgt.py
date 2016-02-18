from ..datasets import datasetsIndex
import os
import zipfile
from redis_utils import r_server
import json

def zipdir(path, zipname):

    ziph = zipfile.ZipFile(zipname, 'w')
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

    ziph.close()

import shutil

class BaseCgt():


    def getStatus(self):
        '''
        - Fetch cgt job status from Redis Hash - "job:cgt:status"
        '''
        jid = self.hypParams["job_id"]
        status = r_server.hget("job:cgt:status", jid) 
        return status

    def writeCGTBinary(self):

        print "Saving CGT_MLP Model to binary"

        try:
            fname = self.jobDir + "/"
            jid = self.hypParams["job_id"]
        except:
            fname = "test1/"


        if not os.path.isfile(fname + "train.inp"):


            self.trainf.save(fname + "train.inp")
            self.paramOut.save(fname + "param.inp")
            self.paramResume.save(fname + "paramResume.inp")
            self.computeloss.save(fname + "valid.inp")

            self.trainf.record(fname + "train_sched.bin")
            self.computeloss.record(fname + "valid_sched.bin")

            # paramsOut = self.paramOut()
            # self.paramResume.record(fname + "params_out")
            # self.paramResume(*paramsOut)
            
            return True 

        return False


    def train(self, X, Y, nepochs, callbacks):
        '''
        - Save model as cgt binary
        - Record training session
        - Make zip of the binaries available
        - Add job to Redis pending queue
        '''

        self.queue_redis()
        try:
            fname = self.jobDir + "/"
            jid = self.hypParams["job_id"]
        except:
            fname = "test1/"


        if not os.path.isfile(fname + "train.inp"):
            self.writeCGTBinary()

            batch_size=128

            for start in xrange(0, X.shape[0], batch_size):
                end = start+batch_size
                print self.trainf(X[start:end], Y[start:end])

            try:
                dataset_id = int(self.hypParams["model"].get("valid", 10))
                DS = datasetsIndex.get(dataset_id)
                dset = DS()
                print self.computeloss(dset.X, dset.Y)
            except:
                pass

            # shutil.make_archive("cgtjobs/" + jid , 'zip', self.jobDir)
        


    def queue_redis(self):

        try:
            fname = self.jobDir + "/"
            jid = self.hypParams["job_id"]
        except:
            jid = "5_0"
            self.jobDir = "./test1"

        zipFolder = "../webserver/cgtjobs/"

        if not os.path.isfile(zipFolder + jid + ".zip"):
            shutil.make_archive(zipFolder + jid , 'zip', self.jobDir)

        jinfo = {
            "Args": jid,
            "Jobid": jid,
            "BinaryKey": "a.out",
            "BinaryKey_Next": "",
        }

        jinfostr = json.dumps(jinfo)
        print "Queueing Redis Job"
        r_server.sadd("job:a.out:pending", jid)
        r_server.hset("job:a.out:args", jid, jinfostr)
        

    def evaluate(self, X, Y, dbg=1):
        '''
        - Fetch latest params from REDIS/WebServer
        - Using those params, evaluate as normal
        '''
        err, cost = self.computeloss(X, Y)
        return err

    def saveWeights(self, fpath=None):

        if fpath == None:
            fpath = self.jobDir + "/params_out"

        print "Saving CGT Weights"
        paramsOut = self.paramOut()
        self.paramResume.record(fpath, *paramsOut)

    
    def loadRedisParams(self):

        try:
            jid = self.hypParams["job_id"]
            prms = r_server.hget("job:cgt:params", jid)
            f = open("tmp.params", 'w')
            f.write(prms)
            f.close()
            self.loadWeights("tmp.params")
        except Exception, e:
            print "\n ERROR: COULDNT LOAD REDIS PARAMS: %s\n" % e

    def loadWeights(self, fpath=None):
        if fpath == None:
            fpath = self.jobDir + "/params_out"

        print "Loading CGT Weights in %s" % fpath
        self.paramResume.runSched(fpath)

    def getSize(self):
        return 0
