from subprocess import Popen, PIPE
import os, signal
from os.path import join
import datetime
from colorama import Fore

class BaseMikov():

    def getSize(self):
        return 0


    def getTempModelFile(self):

        path = "../tmp/"
        fname = "model_%s"%datetime.datetime.now()

        return join(path, fname)


    def train(self, X, Y, nepochs, callbacks):

        print "Started Training Toolkit Model"

        modelFname = join(callbacks[0].job.jobDir , "weights_0")

        progArgs = [
                
            self.execFile,
            "-train '%s'"%X,
            "-valid '%s'"%Y,
            "-rnnlm '%s'"%modelFname,
            "-hidden %d" % self.numHidden,
            "-rand-seed 1 -debug 2 -class 100 -bptt 4 -bptt-block 10 -direct-order 3 -direct 2 -binary",
        ]

        print Fore.CYAN, "Running Command %s" % ' '.join(progArgs) , Fore.WHITE

        p = Popen(' '.join(progArgs), stdout=PIPE, shell=True)

        allOut = ''

        while True:

            pl = p.poll()

            line = p.stdout.read(100)
            allOut += line

            try:
                ln = allOut.split('Iter:')[-2]
                nums = ln.split('  ')
                nums.remove('')
                msg = dict(enumerate(nums))

                if("VALID" in line):
                    print line
                # msg = {
                #         "line": allOut.split('Iter:')[-2],
                # }
            except Exception, e:
                msg = {"line": line}

                print line

            for cb in callbacks:
                cb.on_cmd_update(msg)

            if pl != None and line == '':
                break

            if callbacks[0].checkStop():
                p.kill()

        
        print "Training Complete"

    def evaluate(self, X, Y):
        
        print "Evaluating Mikilov Toolkit Model"

        modelFname = join(self.jobDir , "weights_0")

        progArgs = [
                
            self.execFile,
            "-rnnlm '%s'"%modelFname,
            "-test '%s'"%X,
            "-debug 2",
        ]

        print Fore.CYAN, "Running Command %s" % ' '.join(progArgs) , Fore.WHITE

        p = Popen(' '.join(progArgs), stdout=PIPE, shell=True)

        line = "Some ERROR"

        line = p.stdout.read()

        return line

    def generate(self, num=50):
        
        print "Generating Sequence Mikilov Toolkit Model"

        modelFname = join(self.jobDir , "weights_0")

        progArgs = [
                
            self.execFile,
            "-rnnlm '%s'"%modelFname,
            "-gen %d"%num,
        ]

        print Fore.CYAN, "Running Command %s" % ' '.join(progArgs) , Fore.WHITE

        p = Popen(' '.join(progArgs), stdout=PIPE, shell=True)

        line = "Some ERROR"

        line = p.stdout.read()

        return line

    def saveWeights(self, fpath):

        print "Saving KERAS Weights in %s" % fpath


    def loadWeights(self, fpath):

        print "Loading KERAS Weights in %s" % fpath
