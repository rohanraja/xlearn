from trainer import *
import numpy as np
from colorama import Fore
from os.path import join

def start_evaluation(params):

    mid = params["modelId"]
    pid = params["paramsId"]
    did = params.get("datasetId", 1)
    num = params.get("nsents", 1)
    epoch = params.get("currentEpoch", 1)

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
        
        if int(num) == -4 :
            import trainer
            trainer.startAllTraining(params)
            return ""

        if int(num) == -5 :
            import trainer
            return trainer.startAllEvaluation(params)

        if int(num) == -7 :
            stat = job.model.getStatus()
            return {"status": stat}
            
        if int(num) == -8 :
            job.model.loadRedisParams()
            return {"Test Perplexicity": "%.4f"%job.model.evaluate()}

        if int(num) == -9 :
            job.model.loadRedisParams()
            return {"Sequence": "%s"%job.model.generateSequence()}
        if int(num) == -10 :
            job.model.queue_redis()
            return {}
    except:
        pass
    
    fname = "weights_%s" % epoch 
    job.load_weights(fname)


    out = job.evaluate_dataset(did, num)

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
    job.model.loadRedisParams()
    
    # fname = "weights_%s" % epoch 
    # job.load_weights(fname)



    try:
        perplex = job.evaluate_sentance(sentance)
        return perplex
        out = {
            "perplexicity": "%.2f"%(perplex),
        }
    except Exception,e :
        # out = {
        #     "perplexicity": "%s"%(perplex.split('\n')[-2]),
        # }

        out = {
            "perplexicity": "%s"%e,
        }

    return out



def predict_word_embedding(params):
    mid = params["modelId"]
    pid = params["paramsId"]
    word = params["word"]
    epoch = params["currentEpoch"]

    job = getJob(params)
    job.model.loadRedisParams()
    
    fname = "weights_%s" % epoch 
    job.load_weights(fname)

    return job.evaluate_word_embedding(word)

def predict_next_words(params):
    return {}
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
