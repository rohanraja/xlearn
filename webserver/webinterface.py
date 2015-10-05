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

def getDatasetName(dataId):

    return str(dataId)

def loadDatasets(params):

    projects = project.Project.list()

    # projects = map(lambda p: project.Project(p).getJobInfo(), projects)
    
    outMap = {}

    for p in projects:
        pro = project.Project(p)
        pMap2 = pro.getJobInfo()
        pMap = {}
        pMap["id"] = p
        pMap["name"] = p
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

from ..models import modelsIndex
def models_list(params):
    
    out = []
    
    arr = modelsIndex

    for k in arr:
        obj = {}
        obj["id"] = k
        obj["name"] = arr[k].__name__
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
