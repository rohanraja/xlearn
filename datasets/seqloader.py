import cgt
import numpy as np, numpy.random as nr
nr.seed(0)
import os.path as osp
from basedataset import BaseDataset
from nltk import word_tokenize
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

class Loader(object):
    def __init__(self, data_dir, size_batch, n_unroll, split_fractions, wordSeq = False, num_partitions = 1, worker_id = -1):
        input_file = osp.join(data_dir,"input.txt")
        self.valid_file = osp.join(data_dir,"valid.txt")
        self.test_file = osp.join(data_dir,"test.txt")
        preproc_file = osp.join(data_dir, "preproc_%d.npz"%wordSeq)
        run_preproc = not osp.exists(preproc_file) or osp.getmtime(input_file) > osp.getmtime(preproc_file)
        txt_processor = text_to_tensor_word if wordSeq else text_to_tensor

        self.size_batch = size_batch

        if run_preproc:
        
            txt_processor(input_file, preproc_file)

        data_file = np.load(preproc_file)
        self.char2ind = {char:ind for (ind,char) in enumerate(data_file["chars"])}
        data = data_file["inds"]
        data = data[:data.shape[0] - (data.shape[0] % size_batch)].reshape(size_batch, -1).T # inds_tn
        n_batches = (data.shape[0]-1) // n_unroll 
        data = data[:n_batches*n_unroll+1]  # now t-1 is divisble by batch size
        self.n_unroll = n_unroll
        self.data = data

        self.n_train_batches = int(n_batches*split_fractions[0])
        self.n_test_batches = int(n_batches*split_fractions[1])
        self.n_val_batches = n_batches - self.n_train_batches - self.n_test_batches

        print "%i train batches, %i test batches, %i val batches"%(self.n_train_batches, self.n_test_batches, self.n_val_batches)

        self.test_batches_iter = self.generateGenerator(self.test_file, (self.n_train_batches, self.n_train_batches + self.n_test_batches))
        self.valid_batches_iter = self.generateGenerator(self.valid_file, (self.n_train_batches + self.n_test_batches, self.n_train_batches + self.n_test_batches + self.n_val_batches))

        if worker_id == -1 or worker_id >= num_partitions :
            self.train_range = xrange(self.n_train_batches)
        else:
            chunk_size = self.n_train_batches / num_partitions
            self.train_range = xrange(worker_id*chunk_size , (worker_id+1)*chunk_size )
            print "NumTrainBatches", chunk_size


    def get_data(self, fname):
        f = open(fname, 'r')
        text = f.read()
        inds = []
        for char in tokenize(text):
            ind = self.char2ind.get(char, 0)
            inds.append(ind)
        f.close()
        return inds

    @property
    def size_vocab(self):
        return len(self.char2ind)

    def train_batches_iter(self):
        for i in self.train_range:
            start = i*self.n_unroll
            stop = (i+1)*self.n_unroll
            yield ind2onehot(self.data[start:stop], self.size_vocab), ind2onehot(self.data[start+1:stop+1], self.size_vocab) # XXX

    def generate_iters(self, fname):
        data = np.array(self.get_data(fname))
        data = data[:data.shape[0] - (data.shape[0] % self.size_batch)].reshape(self.size_batch, -1).T
        n_batches = (data.shape[0]-1) // self.n_unroll 
        data = data[:n_batches*self.n_unroll+1]  # now t-1 is divisble by batch size
        return data, n_batches

    def generateGenerator(self, fname, xrnge):
        def f():
            if osp.exists(fname):
                data, n_batches = self.generate_iters(fname)
                iters = xrange(n_batches)
            else:
                data = self.data
                iters = xrange(*xrnge)

            for i in iters:
                start = i*self.n_unroll
                stop = (i+1)*self.n_unroll
                yield ind2onehot(data[start:stop], self.size_vocab), ind2onehot(data[start+1:stop+1], self.size_vocab) # XXX

        return f



# XXX move elsewhere
def ind2onehot(inds, n_cls, isStep = False):
    inds = np.asarray(inds)
    out = np.zeros(inds.shape+(n_cls,),cgt.floatX)
    out.flat[np.arange(inds.size)*n_cls + inds.ravel()] = 1
    if isStep:
        return out
    else:
        return inds


def text_to_tensor(text_file, preproc_file):
    with open(text_file,"r") as fh:
        text = fh.read()
    char2ind = {}
    inds = []
    for char in text:
        ind = char2ind.get(char, -1)
        if ind == -1:
            ind = len(char2ind)
            char2ind[char] = ind
        inds.append(ind)
    np.savez(preproc_file, inds = inds, chars = sorted(char2ind, key = lambda char : char2ind[char]))

def text_to_tensor_word(text_file, preproc_file):
    with open(text_file,"r") as fh:
        text = fh.read()
        import string
        text = filter(lambda x: x in string.printable, text)
    char2ind = {}
    inds = []
    for char in tokenize(text):
        ind = char2ind.get(char, -1)
        if ind == -1:
            ind = len(char2ind)
            char2ind[char] = ind
        inds.append(ind)
    np.savez(preproc_file, inds = inds, chars = sorted(char2ind, key = lambda char : char2ind[char]))

def tokenize(text):

    toks = word_tokenize(text)

    # print "******* NUM WORDS -", len(toks)
    return toks
    return text.split(" ")


class CGT_Sequence(BaseDataset):

    def __init__(self):
        self.l = Loader("../datasets/alice" , 64, 6,(0.1,0.9,0))
        self.X = self.l
        self.Y = []
        # self.X, self.Y  =  self.l.train_batches_iter().next()


