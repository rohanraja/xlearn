from base import *
from scipy.optimize import minimize


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
job.model.loadWeights()

# out = job.model.fprime(job.model.getx())

x0 = job.model.getx()
print job.model.f(x0)

def calb(xnew):
    print job.model.f(xnew)
    job.model.setx(xnew)
    job.model.saveWeights()

minimize(job.model.f, x0, method='cg', jac=job.model.fprime,
                options={'disp': True}, callback = calb)

job.model.loadWeights()

#
# # job.model.updateRedisParams()
# job.model.train()
#

