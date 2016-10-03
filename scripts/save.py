from base import *

cgt_GRU.config["isTraining"] = True
cgt_GRU.config["isLoss"] = True
cgt_GRU.IS_SAVING = True
cgt_GRU.IS_TIMING = False
cgt_GRU.bend = "native"

job = getJob(params)

job.model.loadWeights()

job.model.train()


