from ..datasets import datasetsIndex
import os
import zipfile

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
        return ""

    def train(self, X, Y, nepochs, callbacks):
        '''
        - Save model as cgt binary
        - Record training session
        - Make zip of the binaries available
        - Add job to Redis pending queue
        '''
        print "Saving CGT_MLP Model to binary"

        try:
            fname = self.jobDir + "/"
        except:
            fname = "test1/"
        self.trainf.save(fname + "train.inp")
        self.paramOut.save(fname + "param.inp")
        self.computeloss.save(fname + "valid.inp")
        self.paramResume.save(fname + "paramResume.inp")

        self.trainf.record(fname + "train_sched.bin")
        self.computeloss.record(fname + "valid_sched.bin")

        batch_size=128

        for start in xrange(0, X.shape[0], batch_size):
            end = start+batch_size
            self.trainf(X[start:end], Y[start:end])

        try:
            dataset_id = int(self.hypParams["model"].get("valid", 10))
            DS = datasetsIndex.get(dataset_id)
            dset = DS()
            self.computeloss(dset.X, dset.Y)
        except:
            pass

        jid = self.hypParams["job_id"]
        shutil.make_archive("cgtjobs/" + jid , 'zip', self.jobDir)

    def evaluate(self, X, Y, dbg=1):
        '''
        - Fetch latest params from REDIS/WebServer
        - Using those params, evaluate as normal
        '''
        err, cost = self.computeloss(X, Y)
        return err

    def saveWeights(self, fpath):

        print "Saving CGT Weights in %s" % fpath


    def loadWeights(self, fpath):

        print "Loading CGT Weights in %s" % fpath

    def getSize(self):
        return 0
