from base import *

cgt_GRU.config["isTraining"] = True
cgt_GRU.config["isLoss"] = True
cgt_GRU.IS_SAVING = False
cgt_GRU.IS_TIMING = True
cgt_GRU.bend = "python"

job = getJob(params)

job.model.loadWeights()

job.model.generateSequence()


