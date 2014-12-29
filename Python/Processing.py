import sys
sys.path.append('../libsvm/python')
import numpy as np
from svmutil import *

def Training(data, params):
    param = '-s 2 -t 2 -n ' + str(params[0]) + ' -g ' + str(params[1]) 
    print param
    model = svm_train([1 for _ in range(len(data))], data.tolist(), param)

    p_label, p_acc, p_val = svm_predict([1 for _ in range(len(data))], data.tolist(), model)

    p_val = np.array(p_val).reshape(1, len(p_val)).tolist()[0]

    return model, p_val

def Testing(data, models, p_val):
    for model in models:
        svm_predict([-1 for _ in range(len(data))], data.tolist(), model)
