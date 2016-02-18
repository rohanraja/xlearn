from base import *

cgt_GRU.config["isTraining"] = True
cgt_GRU.config["isLoss"] = True
cgt_GRU.IS_SAVING = False
cgt_GRU.IS_TIMING = True
cgt_GRU.bend = "python"

job = getJob(params)

try:
    job.model.worker_id = int(sys.argv[3])
except Exception, e:
    print e

job.model.loadWeights()

job.model.updateRedisParams()
# job.model.train()


