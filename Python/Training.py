import sys
sys.path.append('../libsvm/python')
import numpy as np
from svmutil import *

def Training(data):
    model = svm_train([1 for _ in range(len(data))], data.tolist(), '-s 2 -t 2 -n 0.0016 -g 0.0129746337890625')

    p_label, p_acc, p_val = svm_predict([1 for _ in range(len(data))], data.tolist(), model)

    p_val = np.array(p_val).reshape(1, len(p_val)).tolist()[0]

    return model, p_val
