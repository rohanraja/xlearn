import numpy as np
from colorama import Fore
import theano
import numpy
import os

from theano import tensor as T
from collections import OrderedDict

class RNN():
    
    def __init__(self, nh, vocab, nc = 6 ):
      
        np.random.seed(10)

        ne = vocab.V
        de = vocab.D

        # parameters of the model
        self.emb = theano.shared(vocab.getWord2VecMatrix().astype(theano.config.floatX)) # add one for PADDING at the end
        self.Wx  = theano.shared(0.2 * numpy.random.uniform(-1.0, 1.0,\
                   (de, nh)).astype(theano.config.floatX))
        self.Wh  = theano.shared(0.2 * numpy.random.uniform(-1.0, 1.0,\
                   (nh, nh)).astype(theano.config.floatX))
        self.W   = theano.shared(0.2 * numpy.random.uniform(-1.0, 1.0,\
                   (nh, nc)).astype(theano.config.floatX))
        self.bh  = theano.shared(numpy.zeros(nh, dtype=theano.config.floatX))
        self.b   = theano.shared(numpy.zeros(nc, dtype=theano.config.floatX))
        self.h0  = theano.shared(numpy.zeros(nh, dtype=theano.config.floatX))

        # bundle
        self.params = [ self.emb, self.Wx, self.Wh, self.W, self.bh, self.b, self.h0 ]
        self.names  = ['embeddings', 'Wx', 'Wh', 'W', 'bh', 'b', 'h0']

    # def initialize_ops(self):

        # Ops definition
        idxs = T.ivector() # as many columns as context window size/lines as words in the sentence
        x = self.emb[idxs].reshape((idxs.shape[0], de))
        y = T.iscalar('y')

        def recurrence(x_t, h_tm1):
            h_t = T.nnet.sigmoid(T.dot(x_t, self.Wx) \
                    + T.dot(h_tm1, self.Wh) + \
                    self.bh)

            s_t = T.nnet.softmax(T.dot(h_t, self.W) + self.b)
            return [h_t, s_t]

        [h, s], _ = theano.scan(fn=recurrence, \
            sequences=x, outputs_info=[self.h0, None], \
            n_steps=x.shape[0])

        p_y_given_x_lastword = s[-1,0,:]
        p_y_given_x_sentence = s[:,0,:]
        y_pred = T.argmax(p_y_given_x_lastword)
        # y_pred = T.argmax(p_y_given_x_sentence, axis=1)

        totalCost = -T.mean(T.log(p_y_given_x_lastword)[y])
        # totalCost = T.mean(costs)

        # def recurrence(x_t, y_t, h_tm1):
        #     h_t = T.nnet.sigmoid(T.dot(x_t, self.Wx) + T.dot(h_tm1, self.Wh) + self.bh)
        #     s_t = T.nnet.softmax(T.dot(h_t, self.W) + self.b)
        #     cost_t = -1.0 *T.log(s_t[0][y_t])
        #     return [h_t, s_t, cost_t]
        #
        # [h, s, costs], _ = theano.scan(fn=recurrence, \
        #     sequences=[x, y], outputs_info=[self.h0, None, None], \
        #     n_steps=x.shape[0])

        # totalCost = T.mean(costs)
        # y_pred = T.argmax(s[2])
        # y_pred = (s.reshape(idxs.shape[0], ne))
        # y_pred = T.argmax(s[:,0,:], axis=1)

        gradients = T.grad(totalCost , self.params)

        lr = T.scalar('lr')
        updates = OrderedDict(( p, p-lr*g ) for p, g in zip( self.params , gradients))

        self.cost = theano.function(inputs=[idxs, y], outputs=totalCost)

        # self.costArray = theano.function(inputs=[idxs, y], outputs=costs)
        
        # theano functions
        self.classify = theano.function(inputs=[idxs], outputs=y_pred)
        #
        self.trainPred = theano.function( inputs  = [idxs, y, lr],
                                      outputs = y_pred,
                                      updates = updates )
        self.train = theano.function( inputs  = [idxs, y, lr],
                                      outputs = totalCost,
                                      updates = updates )



        # #
        self.normalize = theano.function( inputs = [],
                         updates = {self.emb:\
                         self.emb/T.sqrt((self.emb**2).sum(axis=1)).dimshuffle(0,'x')})



        # import pdb; pdb.set_trace()

    def initializeProcs(self):
        p_y_given_x_lastword = s[-1,0,:]
        p_y_given_x_sentence = s[:,0,:]
        y_pred = T.argmax(p_y_given_x_sentence, axis=1)

        # cost and gradients and learning rate
        lr = T.scalar('lr')
        nll = -T.mean(T.log(p_y_given_x_lastword)[y])
        gradients = T.grad( nll, self.params )
        updates = OrderedDict(( p, p-lr*g ) for p, g in zip( self.params , gradients))
        
        # theano functions
        self.classify = theano.function(inputs=[idxs], outputs=y_pred)

        self.train = theano.function( inputs  = [idxs, y, lr],
                                      outputs = nll,
                                      updates = updates )

        self.normalize = theano.function( inputs = [],
                         updates = {self.emb:\
                         self.emb/T.sqrt((self.emb**2).sum(axis=1)).dimshuffle(0,'x')})



    # @staticmethod
    def load(self, fname):

        import cPickle

        # try:
        f = file(fname, 'rb')
        out = cPickle.load(f)
        f.close()

        self.__dict__.update(out)

        # except Exception, e:
            # print "LOADERRER", e
            # pass

    def save(self, fname="rnn.save_bak"):
        import cPickle

        f = file(fname, 'wb')
        g = file('rnn.save', 'wb')
        state = dict(self.__dict__)
        import sys
        sys.setrecursionlimit(5000)
        cPickle.dump(state, f, protocol=cPickle.HIGHEST_PROTOCOL)
        cPickle.dump(state, g, protocol=cPickle.HIGHEST_PROTOCOL)
        f.close()
        g.close()
