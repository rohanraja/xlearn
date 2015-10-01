from ..jobs import project

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

