from trainer import *
import numpy as np
from colorama import Fore
from os.path import join

def start_evaluation(params):

    mid = params["modelId"]
    pid = params["paramsId"]
    did = params["datasetId"]
    num = params["nsents"]
    epoch = params["currentEpoch"]

    job = getJob(params)

    try:
        if int(num) == -1 :
            out = job.model.allOut
            print Fore.YELLOW, out, Fore.WHITE
            return {"": out } 
        if int(num) == -2 :
            f = open( join(job.jobDir, "weights_0.output.txt") , 'r')
            out = f.read()
            f.close()
            print Fore.CYAN, out, Fore.CYAN
            return {"": out } 
        if int(num) == -3 :
            f = open( join(job.jobDir, "log") , 'r')
            out = f.read()
            f.close()
            print Fore.MAGENTA, out, Fore.MAGENTA
            return {"": out } 
    except:
        pass
    
    fname = "weights_%s" % epoch 
    job.load_weights(fname)


    out = job.evaluate_dataset(did, num)
    import pdb; pdb.set_trace()

    f = open( join(job.jobDir, "log") , 'a+')
    f.write("\n" + str(out) + "\n")
    f.close()

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

    try:
        out = {
            "perplexicity": "%.2f"%(perplex),
        }
    except:
        out = {
            "perplexicity": "%s"%(perplex.split('\n')[-2]),
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
