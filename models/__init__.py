from rnn import RNN
from lstm import LSTM_0, MLP_0
from mlp_quant_1 import MLP_QUANT
from svm_quant import *
modelsIndex = {

    0 : RNN,
    1 : LSTM_0,
    2 : MLP_0,
    3 : MLP_QUANT,
    4 : SVM_QUANT,
    5 : DT_Quant,
    6 : RandomForest,
    7 : Adaboost,
    8 : Multinomial,
    9 : ExtraTrees,

}

