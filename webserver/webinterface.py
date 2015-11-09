from ..jobs import project
import trainer

def getModelInfo(params):
    
    mid = params["modelId"]

    p = project.Project(str(mid))
    out = p.getJobInfo()

    return out

def getParamsInfo(params):
    
    mid = params["modelId"]
    pid = params["paramsId"]

    p = project.Project(str(mid))
    out = p.getParamsInfo(str(pid))

    return out

def delete_param(params):
    
    mid = params["modelId"]
    pid = params["paramsId"]

    p = project.Project(str(mid))
    out = p.delete_param(str(pid))

    return out
    

def createParamsInfo(params):

    mid = params["modelId"]
    pInfo = params["pInfo"]

    p = project.Project(str(mid))
    newPid = p.createParamsInfo(pInfo)

    return newPid

def createModelInfo(params):

    mInfo = params["mInfo"]
    pInfo = params["pInfo"]

    newMid = project.Project.createModelInfo(mInfo)
    
    p2 = {"modelId": newMid, "pInfo": pInfo}
    newPid = createParamsInfo(p2)

    return [newMid, newPid]

from ..datasets import datasetsIndex
from ..models import modelsIndex

def getDatasetName(dataId):

    return datasetsIndex[int(dataId)].__name__

def getJobName(pro):

    return modelsIndex[int(pro.jinfo["model_id"])].__name__

def loadDatasets(params):

    projects = project.Project.list()

    # projects = map(lambda p: project.Project(p).getJobInfo(), projects)
    
    outMap = {}

    for p in projects:
        pro = project.Project(p)
        pMap2 = pro.getJobInfo()
        pMap = {}
        pMap["id"] = p
        pMap["name"] = getJobName(pro)
        pMap["params"] = pro.listJobs()
        outMap[pMap2["dataset_id"]] = outMap.get(pMap2["dataset_id"], []) + [pMap]

    out = []
    for k in outMap:

        curr = {}
        curr["name"] = getDatasetName(k)
        curr["id"] = (k)
        curr["models"] = outMap[k]
        out.append(curr)

    return out


def start_training(params):

    trainer.start_training(params)

    return "Started Training"

def stop_training(params):

    trainer.stop_training(params)

    return "Stopped Training"

def get_epoch_list(params):

    return trainer.get_epoch_list(params)



import evaluate

def start_evaluation(params):

    return evaluate.start_evaluation(params)

def test_sentance(params):

    return evaluate.test_sentance(params)

def test_sentance_prediction(params):

    return evaluate.predict_next_words(params)

def generate_sequence(params):

    return evaluate.generate_sequence(params)

def predict_word_embedding(params):

    return evaluate.predict_word_embedding(params)

from ..mappers import mappersIndex
def mappers_list(params):
    
    out = []
    
    arr = mappersIndex

    for k in arr:
        obj = {}
        obj["id"] = k
        obj["name"] = arr[k].__name__
        out.append(obj)

    return out

def get_mapper_stats(params):
    jinfo = getModelInfo(params)

    DS = datasetsIndex[jinfo["dataset_id"]]
    data = DS()
    M = mappersIndex[jinfo["mapper_id"]]
    m = M(data)

    return m.getstats()

def dataset_list(params):
    
    out = []
    
    arr = datasetsIndex

    for k in arr:
        obj = {}
        obj["id"] = k
        obj["name"] = arr[k].__name__
        out.append(obj)

    return out
def search_dataset(params):

    jinfo = getModelInfo(params)
    DS = datasetsIndex[jinfo["dataset_id"]]
    data = DS()
    phrase = params["phrase"]

    return data.search(phrase)

def models_list(params):
    
    out = []
    
    arr = modelsIndex

    for k in arr:
        obj = {}
        obj["id"] = k
        obj["name"] = arr[k].__name__
        try:
            obj["params"] = arr[k].defaultParams()
        except:
            obj["params"] = {}

        out.append(obj)

    return out


from ..embeddings import embeddingsIndex
def embeddings_list(params):
    
    out = []
    
    arr = embeddingsIndex

    for k in arr:
        obj = {}
        obj["id"] = k
        obj["name"] = arr[k].__name__
        out.append(obj)

    return out
