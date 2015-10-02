from ..jobs import project
import keras.callbacks
import tornado.ioloop
import json
import numpy as json

TRAINING_JOBS = {}

from multiprocessing.pool import ThreadPool
poolWorkers = ThreadPool(10)

def getJob(params):

    mid = params["modelId"]
    pid = params["paramsId"]

    p = project.Project(str(mid))

    job = p.getJob(pid)

    return job



class BatchCallBack(keras.callbacks.Callback):

    def __init__(self, jobid):
        self.jobid = jobid

    def on_train_begin(self, logs={}):

        message = {}
        message["status"] = "Trainer Running"
        self.send_message(message)

        if (TRAINING_JOBS[self.jobid]["current_epoch"] > 0):
            self.load_epoch(TRAINING_JOBS[self.jobid]["current_epoch"])
            

        self.model.starting_epoch = TRAINING_JOBS[self.jobid]["current_epoch"] + 1

    def on_batch_end(self, batch, logs={}):
        
        if (TRAINING_JOBS[self.jobid]["stop"]):
            self.model.stop_training = True
        msg = {
                "batch": logs["batch"],
                "totbatches": logs["totalbatches"],
                "epoch": logs["epoch"],
                "totepochs": logs["totepochs"],
                
        }

        self.send_message(msg)

    def on_epoch_end(self, epoch, logs = {}):

        print "Saving Weights from callback"
        fname = "weights_%s" % epoch
        self.job.save_weights(fname)

    def on_train_end(self, logs={}):

        message = {}
        message["status"] = "Training Finished"
        self.send_message(message)


    def send_message(self, message):

        self._send(message) # much better without ioloop
        # try:
        #     ioloop = tornado.ioloop.IOLoop.instance()
        #     ioloop.add_callback(lambda: self._send(message))
        # except:
        #     print "Error in updating handlers"

    def _send(self, message):
        for handler in TRAINING_JOBS[self.jobid]["handlers"] :
            handler(message)


    def load_epoch(self, epoch):
       
        print "Loading Epoch %s" % epoch
        fname = "weights_%s" % epoch
        self.job.load_weights(fname)


def start_training(params):

    jobid = register_training_job(params)
    callback = BatchCallBack(jobid)

    f = lambda : _blocking_trainer(params, callback)
    g = lambda arg : _train_stop(jobid)

    poolWorkers.apply_async(f, (), {}, g)
    #
    # import time
    # time.sleep(20)

def stop_training(params):

    jobid = get_job_id(params)
    TRAINING_JOBS[jobid]["stop"] = True

def _blocking_trainer(params, callback):

    nepochs = params["nepochs"]
    job = getJob(params)
    callback.job = job
    job.start_training(nepochs, callbacks=[callback])

def _train_stop(jobid):

    print "Training of %s Stopped!" % jobid
    del TRAINING_JOBS[jobid]

def get_job_id(params):

    mid = params["modelId"]
    pid = params["paramsId"]

    jobid = "%s_%s"%(mid,pid)
    return jobid


def register_training_job(params):
    
    jobid = get_job_id(params)
    nepochs = params["nepochs"]
    current_epoch = params["currentEpoch"]

    TRAINING_JOBS[jobid] = {
        
            "handlers": [],
            "stop": False,
            "current_epoch": int(current_epoch),
            "total_epochs": nepochs,
    }

    print "\nRegistered Job: %s\n" % jobid
    return jobid



def register_handler(params, handler):

    jobid = get_job_id(params)

    try:
        TRAINING_JOBS[jobid]["handlers"].append(handler)
        print "Attached Hander!!"

        msg = { "status" : "compiling.."}
        handler(msg)
    except:
        print "Failed to attach handler!"

def unregister_handler(params):

    jobid = get_job_id(params)

    try:
        TRAINING_JOBS[jobid]["handlers"] = []
        print "UNREGISTERED Hander!!"
    except:
        print "Failed to attach handler!"


from os.path import join
from os import listdir
import re

def get_epoch_list(params):

    mid = params["modelId"]
    pid = params["paramsId"]
    
    baseDir = "../projects"

    wpath = join(baseDir, str(mid), str(pid))

    weights = []
    
    for val in listdir(wpath):

        try:
            weight = {}
            wid = int(re.findall(r'\d+',val)[0])
            weight["id"] = wid
            weight["name"] = "Weight_%d"%wid
            weights.append(weight) 
        except:
            pass

    weights.sort()

    return weights



