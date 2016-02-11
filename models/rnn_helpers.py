import cgt
from cgt import nn
from cgt.distributions import categorical
import numpy as np
from cgt import nn, utils, profiler
import numpy as np, numpy.random as nr
from StringIO import StringIO
from param_collection import ParamCollection
from colorama import Fore


config = {

    'isTraining' :False,
    'isLoss' : False,
}

def make_bi_simple_rnn(size_input, size_mem, n_layers, size_output, size_batch):
    print "Building Bidirectional Simple RNN Network"
    inputs = [cgt.matrix() for i_layer in xrange(n_layers+1)]
    outputs = []
    for i_layer in xrange(n_layers):
        prev_h = inputs[i_layer+1] # note that inputs[0] is the external input, so we add 1
        x = inputs[0] if i_layer==0 else outputs[i_layer-1]
        size_x = size_input if i_layer==0 else size_mem

        next_h = cgt.sigmoid(
            nn.Affine(size_x, size_mem,name="i2u")(x)
            + nn.Affine(size_mem, size_mem, name="h2u")(prev_h))
        outputs.append(next_h)

    # category_activations = nn.Affine(size_mem, size_output,name="pred")(outputs[-1])
    # logprobs = nn.logsoftmax(category_activations)
    # outputs.append(logprobs)

    return nn.Module(inputs, outputs)

def make_simple_rnn(size_input, size_mem, n_layers, size_output, size_batch, bi=False):
    print "Building Simple RNN Network"
    inputs = [cgt.matrix() for i_layer in xrange(n_layers+1)]
    outputs = []
    for i_layer in xrange(n_layers):
        prev_h = inputs[i_layer+1] # note that inputs[0] is the external input, so we add 1
        x = inputs[0] if i_layer==0 else outputs[i_layer-1]
        size_x = size_input if i_layer==0 else size_mem

        next_h = cgt.sigmoid(
            nn.Affine(size_x, size_mem,name="i2u")(x)
            + nn.Affine(size_mem, size_mem, name="h2u")(prev_h))
        outputs.append(next_h)

    if bi == False:
      category_activations = nn.Affine(size_mem, size_output,name="pred")(outputs[-1])
      logprobs = nn.logsoftmax(category_activations)
      outputs.append(logprobs)

    return nn.Module(inputs, outputs)

def make_deep_lstm(size_input, size_mem, n_layers, size_output, size_batch, bi=False):
    inputs = [cgt.matrix(fixed_shape=(size_batch, size_input))]
    for _ in xrange(n_layers):
        inputs.append(cgt.matrix(fixed_shape=(size_batch, size_mem)))
    outputs = []
    for i_layer in xrange(n_layers/2):
        prev_h = inputs[i_layer*2]
        prev_c = inputs[i_layer*2+1]
        if i_layer==0:
            x = inputs[0]
            size_x = size_input
        else:
            x = outputs[(i_layer-1)*2]
            size_x = size_mem
        input_sums = nn.Affine(size_x, 4*size_mem)(x) + nn.Affine(size_x, 4*size_mem)(prev_h)
        sigmoid_chunk = cgt.sigmoid(input_sums[:,0:3*size_mem])
        in_gate = sigmoid_chunk[:,0:size_mem]
        forget_gate = sigmoid_chunk[:,size_mem:2*size_mem]
        out_gate = sigmoid_chunk[:,2*size_mem:3*size_mem]
        in_transform = cgt.tanh(input_sums[:,3*size_mem:4*size_mem])
        next_c = forget_gate*prev_c + in_gate * in_transform
        next_h = out_gate*cgt.tanh(next_c)
        outputs.append(next_c)
        outputs.append(next_h)

    if bi == False:
      category_activations = nn.Affine(size_mem, size_output)(outputs[-1])
      logprobs = nn.logsoftmax(category_activations)
      outputs.append(logprobs)

    return nn.Module(inputs, outputs)
def make_deep_gru(size_input, size_mem, n_layers, size_output, size_batch, bi=False):
    print "Building GRU Network"
    # import ipdb; ipdb.set_trace()
    inputs = [cgt.matrix() for i_layer in xrange(n_layers+1)]
    outputs = []
    for i_layer in xrange(n_layers):
        prev_h = inputs[i_layer+1] # note that inputs[0] is the external input, so we add 1
        x = inputs[0] if i_layer==0 else outputs[i_layer-1]
        size_x = size_input if i_layer==0 else size_mem
        update_gate = cgt.sigmoid(
            nn.Affine(size_x, size_mem,name="i2u")(x)
            + nn.Affine(size_mem, size_mem, name="h2u")(prev_h))
        reset_gate = cgt.sigmoid(
            nn.Affine(size_x, size_mem,name="i2r")(x)
            + nn.Affine(size_mem, size_mem, name="h2r")(prev_h))
        gated_hidden = reset_gate * prev_h
        p2 = nn.Affine(size_mem, size_mem)(gated_hidden)
        p1 = nn.Affine(size_x, size_mem)(x)
        hidden_target = cgt.tanh(p1+p2)
        next_h = (1.0-update_gate)*prev_h + update_gate*hidden_target
        outputs.append(next_h)
    
    if bi == False:
      category_activations = nn.Affine(size_mem, size_output,name="pred")(outputs[-1])
      logprobs = nn.logsoftmax(category_activations)
      outputs.append(logprobs)

    return nn.Module(inputs, outputs)

networks_dict = {
        "gru" : make_deep_gru,
        "simple": make_simple_rnn,
        "lstm": make_deep_lstm,
}

def ind2onehot_cgt(inds, n_cls):
    out = cgt.zeros(( inds.shape[0] , inds.shape[1] , n_cls))
    slinds = cgt.arange(inds.shape[0]*inds.shape[1] )*n_cls  + inds.flatten()
    ee = cgt.ones(slinds.shape)
    d = cgt.inc_subtensor(out.flatten(), slinds , ee)
    o = d.reshape(( inds.shape[0] , inds.shape[1] , n_cls))
    return o

def make_loss_and_grad_and_step(arch,
        size_input, size_output, size_mem, size_batch, n_layers, n_unroll, bi=True):
    # symbolic variables

    x_inp = cgt.matrix(dtype='int')
    # x_inp = cgt.shared( np.array([[3,2,5] ,[4,1,0]]) ) #cgt.shared(np.ones((3,3)))
    # x_inp = cgt.shared(np.array(np.ones((3,3))))
    y_inp = cgt.matrix(dtype='int')
    # y_inp = cgt.shared( np.array([[3,2,5] ,[4,1,0]]) ) #cgt.shared(np.ones((3,3)))

    x_tnk = ind2onehot_cgt(x_inp, size_input)
    targ_tnk = ind2onehot_cgt(y_inp, size_input)
    # x_tnk = cgt.tensor3()
    # targ_tnk = cgt.tensor3()

    make_network = networks_dict[arch]

    if arch == "lstm":
      n_layers= n_layers * 2

    print n_layers
    # if bi == True:
    #   if arch == "simple":
    #     make_network = make_bi_simple_rnn
    #   if arch == "lstm":
    #     make_network = make_bi_lstm
    #   if arch == "gru":
    #     make_network = make_bi_gru

    network = make_network(size_input, size_mem, n_layers, size_output, size_batch, bi)
    network2 = make_network(size_input, size_mem, n_layers, size_output, size_batch, bi)

    init_hiddens = [cgt.shared(np.ones((size_batch, size_mem))) for _ in xrange(n_layers)]
    init_hiddens2 = [cgt.matrix() for _ in xrange(n_layers)]

    givens = [(ih,np.ones((size_batch, size_mem))) for ih in init_hiddens2]

    cur_hiddens = init_hiddens2
    loss = 0

    forw_hiddens = []

    for t in xrange(n_unroll):
        outputs = network([x_tnk[t]] + cur_hiddens)
        if bi == False :
            cur_hiddens, prediction_logprobs = outputs[:-1], outputs[-1]
            loss = loss - (prediction_logprobs*targ_tnk[t]).sum()
        else:
            cur_hiddens = outputs
            forw_hiddens.append(cur_hiddens[-1])


    forw_hiddens.append(init_hiddens2[-1])
    
    cur_hiddens = init_hiddens2
    if bi == True:
        catAff = nn.Affine(2*size_mem, size_output,name="pred")
        # for t in reversed(xrange(n_unroll)):
        for t in xrange(n_unroll-1 , -1, -1):
            outputs = network2([targ_tnk[t]] + cur_hiddens)
            cur_hiddens = outputs
            
            concat_hiddens = cgt.concatenate([ cur_hiddens[-1] , forw_hiddens[t-1]], axis=1)

            category_activations = catAff(concat_hiddens)
            prediction_logprobs = nn.logsoftmax(category_activations)
            loss = loss - (prediction_logprobs*x_tnk[t]).sum()


    final_hiddens = cur_hiddens

    loss = loss / (n_unroll * size_batch)

    params = network.get_parameters()

    if bi == True:
        params += network2.get_parameters()
        params += [catAff.weight]


    gradloss = cgt.grad(loss, params)
    updates = []

    alpha = cgt.scalar()

    for (parm, grd) in zip(params, gradloss):
      up = (parm, parm - alpha*grd)
      updates.append(up)

    hidupdates = []
    for (hid, curhid) in zip(init_hiddens, final_hiddens):
      up = (hid, hid/hid - 1 + curhid)
      hidupdates.append(up)

    # updates = updates + hidupdates
    flatgrad = cgt.concatenate([x.flatten() for x in gradloss])

    # for p in params:
    #     import ipdb; ipdb.set_trace()

    with utils.Message("compiling loss+grad"):
        # f_loss_and_grad = cgt.function([alpha, x_tnk, targ_tnk] , [loss + flatgrad] + final_hiddens, updates = updates, givens=givens)
        if config["isTraining"]:
          f_loss_and_grad =  cgt.function([alpha, x_inp, y_inp] , [loss + flatgrad] + final_hiddens, updates = updates, givens=givens)
          f_loss = cgt.function(inputs=[x_inp, y_inp] , outputs=[loss], givens=givens)
        else:
          f_loss_and_grad =  None #
          f_loss = None #

          if config["isLoss"]:
            f_loss = cgt.function(inputs=[x_inp, y_inp] , outputs=[loss], givens=givens)

        # f_loss = cgt.function(inputs=[x_tnk, targ_tnk] , outputs=[loss], givens=givens)

    assert len(init_hiddens) == len(final_hiddens)


    if bi == True:
        init_hiddens = [cgt.matrix() for _ in xrange(n_layers)]
        init_hiddens2 = [cgt.matrix() for _ in xrange(n_layers)]
        x_nk = cgt.matrix('x')
        x_nk2 = cgt.matrix('x2')
        
        outputs = network([x_nk] + init_hiddens)
        outputs2 = network2([x_nk2] + init_hiddens2)

        h1 = cgt.matrix()
        h2 = cgt.matrix()
        concat_hiddens = cgt.concatenate([ h2,h1 ], axis=1)
        category_activations = catAff(concat_hiddens)
        prediction_logprobs = nn.logsoftmax(category_activations)

        f_step1 = cgt.function([x_nk] + init_hiddens , outputs)
        f_step2 = cgt.function([x_nk2] + init_hiddens2 , outputs2)
        f_step3 = cgt.function([h2,h1], [prediction_logprobs])
        f_step = [f_step1, f_step2, f_step3]

    else:
        init_hiddens2 = [cgt.matrix() for _ in xrange(n_layers)]
        x_nk = cgt.matrix('x')
        outputs = network([x_nk] + init_hiddens2)
        f_step = cgt.function([x_nk] + init_hiddens2 , outputs)

    paramInp = [ cgt.matrix() for i in range(len(params))] 
    pUpdates = []
    for pinp, prm in zip(paramInp, params):
        pUpdates.append((prm, prm - prm + pinp))

    paramResume = cgt.function(inputs=paramInp, outputs=[], updates = pUpdates)
    paramOut = cgt.function(inputs=[], outputs=params)

    return network, f_loss, f_loss_and_grad, f_step, paramResume, paramOut


def cat_sample(ps):    
    """
    sample from categorical distribution
    ps is a 2D array whose rows are vectors of probabilities
    """
    r = nr.rand(len(ps))
    out = np.zeros(len(ps),dtype='i4')
    cumsums = np.cumsum(ps, axis=1)
    for (irow,csrow) in enumerate(cumsums):
        for (icol, csel) in enumerate(csrow):
            if csel > r[irow]:
                out[irow] = icol
                break
    return out

def ind2onehot(inds, n_cls):
    inds = np.asarray(inds)
    out = np.zeros(inds.shape+(n_cls,),cgt.floatX)
    out.flat[np.arange(inds.size)*n_cls + inds.ravel()] = 1
    return out

def sample(f_step, init_hiddens, char2ind, n_steps, temperature, seed_text = "", isWord = False):
    vocab_size = len(char2ind)
    ind2char = {ind:char for (char,ind) in char2ind.iteritems()}
    cur_hiddens = init_hiddens
    t = StringIO()
    t.write(seed_text)
    for char in seed_text:
        x_1k = ind2onehot([char2ind[char]], vocab_size)
        net_outputs = f_step(x_1k, cur_hiddens)
        cur_hiddens, logprobs_1k = net_outputs[:-1], net_outputs[-1]

    if len(seed_text)==0:
        logprobs_1k = np.zeros((1,vocab_size))
    

    for _ in xrange(n_steps):        
        logprobs_1k /= temperature
        probs_1k = np.exp(logprobs_1k*2)
        probs_1k /= probs_1k.sum()
        index = cat_sample(probs_1k)[0]
        char = ind2char[index]
        x_1k = ind2onehot([index], vocab_size)
        net_outputs = f_step(x_1k, *cur_hiddens)
        cur_hiddens, logprobs_1k = net_outputs[:-1], net_outputs[-1]
        # print logprobs_1k
        # return
        t.write(char)
        if isWord :
            t.write(" ")

    val = t.getvalue()
    cgt.utils.colorprint(cgt.utils.Color.YELLOW, val + "\n")
    return val

