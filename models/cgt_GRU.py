from baseCgt import BaseCgt

from rnn_helpers import *
import cgt
from cgt import nn
from cgt.distributions import categorical
import numpy as np
from cgt import nn, utils, profiler
import numpy as np, numpy.random as nr
from StringIO import StringIO
from param_collection import ParamCollection
from colorama import Fore
nr.seed(0)
from ..datasets.seqloader import *
from cgt import profiler
CUP = '\x1b[1A'
ER = '\x1b[2K'
NL = CUP + ER

IS_PROFILE = False
bend = "python" if IS_PROFILE else "native"
IS_SAVING = True
IS_TIMING = False
import time

class BaseCgtRNN(BaseCgt):

    def train(self, *othargs):

        self.check_init()

        loader = self.loader #othargs[0]

        if IS_SAVING:
            isSaved = self.writeCGTBinary()
        else:
            isSaved = True


        for iepoch in xrange(40):
            losses = []
            print "starting epoch",iepoch
            numm = 0
            for (x,y) in loader.train_batches_iter():

                if numm == 1 and IS_PROFILE :
                    profiler.start()

                if IS_TIMING:
                    st = time.time()

                try:
                    out = self.trainf(0.9, x,y)
                except KeyboardInterrupt:
                    self.updateRedisParams()
                    sys.exit(0)

                if IS_TIMING:
                    end = time.time()
                    print "Time Taken: %s Seconds" % (end - st)

                if numm == 1 and IS_PROFILE :
                    profiler.print_stats()
                    return
                numm += 1
                if (not IS_SAVING) and numm%5 == 0:
                    self.updateRedisParams()

                try:
                    loss = out[0]
                    losses.append(loss)
                    print np.exp(loss), np.exp(np.mean(losses))
                except:
                    pass

            if losses == []:
                self.eval_iter = loader.valid_batches_iter
                self.evaluate(loader)
                self.eval_iter = loader.test_batches_iter
                break
            # self.evaluate(loader)
            # self.generateSequence(loader)
            print np.exp(np.mean(losses))
            self.updateRedisParams()


        self.queue_redis()

        self.trainf.finish_record()
        self.computeloss.finish_record()
        self.paramResume.finish_record()

    def evaluate(self, *othargs):

        self.check_init()

        loader = self.loader #othargs[0]
        losses = []
        for (x,y) in self.eval_iter():
            out = self.computeloss(x,y)
            losses.append(out)

            if out != None :
                ppx = np.exp(np.mean(losses))
                print NL , ppx

        try:
            ppx = np.exp(np.mean(losses))
            print Fore.YELLOW, "test ppx =",  ppx
            return ppx
        except:
            return 0.0

    def evaluate_sentance_bi(self, *othargs):
        

        # self.loadRedisParams()

        loader = self.loader #othargs[0]
        sentance = othargs[0]
        words = tokenize(sentance)
        words.append(".")

        cur_hiddens = self.initialize_hiddens(1)
        cur_hiddens2 = self.initialize_hiddens(1)

        n_steps = len(words)
        vocab_size = loader.size_vocab
        ind2char = {ind:char for (char,ind) in loader.char2ind.iteritems()}

        losses = []
        outMap = []

        forw_hiddens = []

        for i in xrange(n_steps - 1):        

            index = loader.char2ind.get(words[i], 0)
            x_1k = ind2onehot([index], vocab_size, True)
            net_outputs = self.f_step[0](x_1k, *cur_hiddens)
            cur_hiddens= net_outputs
            forw_hiddens.append(cur_hiddens[-1])

            
        for i in xrange(n_steps - 2, 0, -1):        

            # import ipdb; ipdb.set_trace()
            index = loader.char2ind.get(words[i+1], 0)
            x_1k = ind2onehot([index], vocab_size, True)
            net_outputs = self.f_step[1](x_1k, *cur_hiddens2)
            cur_hiddens2= net_outputs

            logprobs_1k = self.f_step[2](cur_hiddens2[-1] , forw_hiddens[i-1] )[0]

            tarIdx = loader.char2ind.get(words[i], 0)
            loss = -1 * logprobs_1k[0][tarIdx]
            losses.append(loss)
            probs_1k = np.exp(logprobs_1k*2)
            probs_1k /= probs_1k.sum()
            wordPreds = probs_1k[0]


            topNWords = wordPreds.argsort()[-9:]
            topNWords = topNWords[::-1]
            topNProbabs = wordPreds[topNWords]
            topNProbabs = map(lambda p: "%.3f"%p, topNProbabs)
            topNProbabs.insert(0, "%.3f" % wordPreds[loader.char2ind.get(words[i],0) ])

            topNWords = map(lambda wid: "%s(%d)" % (ind2char[wid], wid), topNWords)
            topNWords.insert(0, words[i])

            omap = {}
            val = "%s(%d)" % (words[i], tarIdx)
            omap[val] = zip(topNWords, topNProbabs)
            outMap.append(omap)
            # import pprint
            # pp = pprint.PrettyPrinter(indent=4)
            # pp.pprint(omap)
            # pp.pprint([words[i-1], words[i+1]])
        
        try:
            ppx = np.exp(np.mean(losses))
            # print Fore.YELLOW, "test ppx =",  ppx
            out = {"Perplexity": "%.2f" % ppx}
            return [out, list(reversed(outMap)) ]
        except:
            return 420.22
    def evaluate_sentance_single(self, *othargs):
        

        # self.loadRedisParams()

        loader = self.loader #othargs[0]
        sentance = othargs[0]
        words = tokenize(sentance)
        words.append(".")

        cur_hiddens = self.initialize_hiddens(1)

        n_steps = len(words)
        vocab_size = loader.size_vocab
        ind2char = {ind:char for (char,ind) in loader.char2ind.iteritems()}

        losses = []
        outMap = []

        for i in xrange(n_steps - 1):        

            index = loader.char2ind.get(words[i], 0)
            x_1k = ind2onehot([index], vocab_size, True)
            net_outputs = self.f_step(x_1k, *cur_hiddens)
            cur_hiddens, logprobs_1k = net_outputs[:-1], net_outputs[-1]
            # probs_1k = np.exp(logprobs_1k*2)
            # probs_1k /= probs_1k.sum()
            tarIdx = loader.char2ind.get(words[i+1], 0)
            loss = -1 * logprobs_1k[0][tarIdx]
            losses.append(loss)
            probs_1k = np.exp(logprobs_1k*2)
            probs_1k /= probs_1k.sum()
            wordPreds = probs_1k[0]


            topNWords = wordPreds.argsort()[-10:]
            topNWords = topNWords[::-1]
            topNProbabs = wordPreds[topNWords]
            topNProbabs = map(lambda p: "%.3f"%p, topNProbabs)


            topNWords = map(lambda wid: "%s(%d)" % (ind2char[wid], wid), topNWords)

            omap = {}
            val = "%s(%d)" % (words[i], index)
            omap[val] = zip(topNWords, topNProbabs)
            outMap.append(omap)
        
        try:
            ppx = np.exp(np.mean(losses))
            print Fore.YELLOW, "test ppx =",  ppx
            out = {"Perplexity": "%.2f" % ppx}
            return [out, outMap]
        except:
            return 420.22
        
    def generateSequence(self, *othargs):

        loader = self.loader #othargs[0]


        if self.word_tokens == 0:
            nstps = 1000
        else:
            nstps = 100

        return sample(self.f_step, self.initialize_hiddens(1), char2ind=loader.char2ind, n_steps=nstps, temperature=1, seed_text = "", isWord = bool(self.word_tokens) )

    def loadHypParam(self, paramName):
        outd = self.defaultParams()[paramName]
        try:
            out = self.hypParams["model"][paramName]
        except:
            out = outd

        out = type(outd)(out)
        setattr(self, paramName, out)
        return out

    def loadAllHypParams(self):
        for k in self.defaultParams():
            self.loadHypParam(k)


class CGT_GRU_RNN(BaseCgtRNN):


    def __init__(self, hyperParams=None, *otherargs):
        

        self.hypParams = hyperParams

        self.is_initialized = False

        self.worker_id = 5


    def check_init(self):

        if self.is_initialized:
            return
        else:
            self.initialize()
            self.is_initialized = True

    def initialize(self):

        print "Initializing CGT_RNN Model"
        cgt.update_config(default_device=cgt.core.Device(devtype="cpu"), backend=bend)

        self.loadAllHypParams()

        if self.bi == 1:
            self.evaluate_sentance = self.evaluate_sentance_bi
        else:
            self.evaluate_sentance = self.evaluate_sentance_single

        self.num_hidden_units = 2 * self.n_layers if self.rnn_type == "lstm" else self.n_layers

        print self.worker_id

        self.loader = Loader(
                self.data_dir, 
                self.size_batch, 
                self.n_unroll, 
                (self.train_split, self.valid_split),
                bool(self.word_tokens),
                self.num_workers,
                self.worker_id
        )

        # if self.valid_split == 0.0:
        #     self.eval_iter = self.loader.train_batches_iter
        # else:

        self.eval_iter = self.loader.test_batches_iter

        self.size_vocab = self.loader.size_vocab

        network, f_loss, f_loss_and_grad, self.f_step, self.paramResume, self.paramOut = make_loss_and_grad_and_step(
                self.rnn_type, 
                self.size_vocab, 
                self.size_vocab, 
                self.size_mem, 
                self.size_batch, 
                self.n_layers, 
                self.n_unroll,
                self.bi,
                )

        self.params = network.get_parameters()

        self.computeloss = f_loss
        self.trainf = f_loss_and_grad
        
        params = network.get_parameters()
        pc = ParamCollection(params)
        pcInit = nr.uniform(-.1, .1, size=(pc.get_total_size(),))
        # pcInit = np.ones((pc.get_total_size(),))
        pc.set_value_flat(pcInit)

        # self.loadRedisParams()


        def initialize_hiddens(n):
            return [np.ones((n, self.size_mem), cgt.floatX) for _ in xrange(self.num_hidden_units)]

        self.initialize_hiddens = initialize_hiddens 

    @staticmethod
    def defaultParams():

        out = {
                "size_mem": 64,
                "size_batch": 64,
                "n_layers": 1,
                "n_unroll": 20,
                "data_dir": "../datasets/alice",
                "train_split": 1.0,
                "valid_split": 0.0,
                "word_tokens": 1,
                "rnn_type": "gru",
                "bi": 0,
                "num_workers": 5,
        }

        return out
