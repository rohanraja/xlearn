from baseCgt import BaseCgt

import cgt
from cgt import nn
from cgt.distributions import categorical
import numpy as np

def init_weights(*shape):
    wval = np.random.randn(*shape) * 0.01
    ww = cgt.shared(wval, fixed_shape_mask='all')
    return ww

def rmsprop_updates(cost, params, stepsize=0.001, rho=0.9, epsilon=1e-6):
    grads = cgt.grad(cost, params)
    updates = []
    for p, g in zip(params, grads):
        acc = cgt.shared(p.op.get_value() * 0.)
        acc_new = rho * acc + (1 - rho) * cgt.square(g)
        gradient_scaling = cgt.sqrt(acc_new + epsilon)
        # g = g / gradient_scaling
        # g = g / gradient_scaling
        updates.append((acc, acc_new))
        updates.append((p, p - stepsize * g))
    return updates, grads

def dense_model(X, w_h, w_h2, w_o, p_drop_input, p_drop_hidden):
    X = nn.dropout(X, p_drop_input)
    h = nn.rectify(cgt.dot(X, w_h))

    h = nn.dropout(h, p_drop_hidden)
    h2 = nn.rectify(cgt.dot(h, w_h2))

    h2 = nn.dropout(h2, p_drop_hidden)
    py_x = nn.softmax(cgt.dot(h2, w_o))
    return py_x

class CGT_MLP(BaseCgt):

    def __init__(self, hyperParams=None):
        
        print "Initializing CGT_MLP Model"

        cgt.update_config(default_device=cgt.core.Device(devtype="cpu"), backend="native")

        self.hypParams = hyperParams

        X = cgt.matrix("X", fixed_shape=(None,28*28))
        y = cgt.vector("y",dtype='i8')

        p_drop_input,p_drop_hidden = (0, 0)
        w_h = init_weights(784, 256)
        w_h2 = init_weights(256, 256)
        w_o = init_weights(256, 10)
        pofy_drop = dense_model(X, w_h, w_h2, w_o, p_drop_input, p_drop_hidden)
        pofy_nodrop = dense_model(X, w_h, w_h2, w_o, 0., 0.)
        params = [w_h, w_h2, w_o]        

        cost_drop = -cgt.mean(categorical.loglik(y, pofy_drop))
        updates, gradss= rmsprop_updates(cost_drop, params, stepsize=0.1)

        y_nodrop = cgt.argmax(pofy_nodrop, axis=1)
        cost_nodrop = -cgt.mean(categorical.loglik(y, pofy_nodrop))
        err_nodrop = cgt.cast(cgt.equal(y_nodrop, y), cgt.floatX).mean() * 100

        paramInp = [ cgt.matrix() for i in range(len(params))] 
        pUpdates = []
        for pinp, prm in zip(paramInp, params):
            pUpdates.append((prm, prm - prm + pinp))

        self.paramResume = cgt.function(inputs=paramInp, outputs=[], updates = pUpdates)
        self.computeloss = cgt.function(inputs=[X, y], outputs=[err_nodrop,cost_nodrop])
        self.trainf = cgt.function(inputs=[X, y], outputs=[cost_nodrop], updates=updates)
        self.paramOut = cgt.function(inputs=[], outputs=params)
        

    @staticmethod
    def defaultParams():

        out = {
                "bptt": 4,
                "class": 100,
                "hidden_nodes": 100,
                "oldclass": 0,
                "flags" : "-rand-seed 1 -debug 2 -bptt-block 10 -direct-order 3 -direct 2 -binary"
        }

        return out
