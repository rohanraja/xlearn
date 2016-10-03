from base import *
from wordvecs import wordVecs

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

job.model.check_init()
job.model.init_wordvecs(wordVecs)
job.model.saveWeights()
import pdb; pdb.set_trace()

job.model.loadWeights()

import pdb; pdb.set_trace()

# job.model.updateRedisParams()

job.model.train()


