from ..jobs import project
from ..models.keras_custom import callbacks
import tornado.ioloop
import json
import numpy as json
import time

TRAINING_JOBS = {}

from multiprocessing.pool import ThreadPool
poolWorkers = ThreadPool(10)

CACHED_JOBS = {}

from colorama import Fore
def getJob(params):

    mid = params["modelId"]
    pid = params["paramsId"]

    jid = "%s_%s" % (mid, pid)
    p = project.Project(str(mid))

    try:
        job = CACHED_JOBS[jid]
        print Fore.GREEN, "\nGOT job from cache. Yay!", Fore.WHITE
    except:
        print Fore.RED, "\nJob not memcached! Creating!!", Fore.WHITE
        job = p.getJob(pid)
        CACHED_JOBS[jid] = job


    return job



class BatchCallBack(callbacks.Callback):

    def __init__(self, jobid):
        self.jobid = jobid

    def on_train_begin(self, logs={}):

        message = {}
        message["status"] = "Trainer Running"
        self.send_message(message)

        if (TRAINING_JOBS[self.jobid]["current_epoch"] > 0):
            self.load_epoch(TRAINING_JOBS[self.jobid]["current_epoch"])
            

        self.model.starting_epoch = TRAINING_JOBS[self.jobid]["current_epoch"] + 1
        self.t1 = time.time()

    def on_batch_end(self, batch, logs={}):
        
        if (TRAINING_JOBS[self.jobid]["stop"]):
            self.model.stop_training = True

        timeTaken = "%.3f seconds" % (time.time() - self.t1)
        self.t1 = time.time()
        msg = {
                "batch": logs["batch"],
                "totbatches": logs["totalbatches"],
                "epoch": logs["epoch"],
                "totepochs": logs["totepochs"],
                "loss": "%.4f"%logs["loss"],
                "acc": "%.2f %%"%(logs["acc"]*100.0),
                "batch time taken": timeTaken,
                
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

    f = lambda : blocking_trainer(params, callback)
    g = lambda arg : _train_stop(jobid)

    poolWorkers.apply_async(f, (), {}, g)
    #
    # import time
    # time.sleep(20)

def stop_training(params):

    jobid = get_job_id(params)
    TRAINING_JOBS[jobid]["stop"] = True

def blocking_trainer(params, callback):

    nepochs = int(params["nepochs"])
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
    nepochs = int(params["nepochs"])
    current_epoch = int(params["currentEpoch"])

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
        # print "Attached Hander!!"

        msg = { "status" : "compiling.."}
        handler(msg)
    except:
        # print "Failed to attach handler!"
        pass

def unregister_handler(params):

    jobid = get_job_id(params)

    try:
        TRAINING_JOBS[jobid]["handlers"] = []
        # print "UNREGISTERED Hander!!"
    except:
        # print "Failed to attach handler!"
        pass


from os.path import join
from os import listdir
import re

import os
import datetime
def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)

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

            modTime = modification_date(join(wpath, val))
            weight["name"] = "Epoch: %d  -  %s"% (wid, modTime)
            weights.append(weight) 
        except:
            pass

    weights.sort()

    return weights



