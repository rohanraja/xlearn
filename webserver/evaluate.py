from trainer import *

def start_evaluation(params):

    mid = params["modelId"]
    pid = params["paramsId"]
    did = params["datasetId"]
    epoch = params["currentEpoch"]

    job = getJob(params)
    
    fname = "weights_%s" % epoch 
    job.load_weights(fname)


    loss, accuracy = job.evaluate_dataset(did)

    out = {
        "loss": "%.4f"%loss,
        "accuracy": "%.2f %%"%(accuracy*100),
    }


    return out
