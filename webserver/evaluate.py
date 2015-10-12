from trainer import *
import numpy as np

def start_evaluation(params):

    mid = params["modelId"]
    pid = params["paramsId"]
    did = params["datasetId"]
    num = params["nsents"]
    epoch = params["currentEpoch"]

    job = getJob(params)
    
    fname = "weights_%s" % epoch 
    job.load_weights(fname)


    mean, std, psingle = job.evaluate_dataset(did, num)
    out = {
        "Perplexicity Mean": mean,
        "Perplexicity Standard Deviation": std,
        "Perplexicity Single Sequence": psingle,
    }

    # loss, accuracy = job.evaluate_dataset(did)
    #
    # out = {
    #     "loss": "%.4f"%loss,
    #     "accuracy": "%.2f %%"%(accuracy*100),
    #     "exp_loss": "%.2f"%(np.exp(loss)),
    #     "exp2_loss": "%.2f"%(np.exp2(loss)),
    # }


    return out


def test_sentance(params):

    mid = params["modelId"]
    pid = params["paramsId"]
    sentance = params["sentance"]
    epoch = params["currentEpoch"]

    job = getJob(params)
    
    fname = "weights_%s" % epoch 
    job.load_weights(fname)


    perplex = job.evaluate_sentance(sentance)

    out = {
        # "loss": "%.4f"%loss,
        # "accuracy": "%.2f %%"%(accuracy*100),
        # "exp_loss": "%.2f"%(np.exp(loss)),
        # "exp2_loss": "%.2f"%(np.exp2(loss)),
        "perplexicity": "%.2f"%(perplex),
    }


    return out



def predict_word_embedding(params):
    mid = params["modelId"]
    pid = params["paramsId"]
    word = params["word"]
    epoch = params["currentEpoch"]

    job = getJob(params)
    
    fname = "weights_%s" % epoch 
    job.load_weights(fname)

    return job.evaluate_word_embedding(word)

def predict_next_words(params):
    mid = params["modelId"]
    pid = params["paramsId"]
    sentance = params["sentance"]
    epoch = params["currentEpoch"]

    job = getJob(params)
    
    fname = "weights_%s" % epoch 
    job.load_weights(fname)

    return job.predict_sentance(sentance)

def generate_sequence(params):
    mid = params["modelId"]
    pid = params["paramsId"]
    epoch = params["currentEpoch"]

    job = getJob(params)
    
    fname = "weights_%s" % epoch 
    job.load_weights(fname)

    return job.generate_sentance()
