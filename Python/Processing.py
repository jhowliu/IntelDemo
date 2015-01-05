import sys
sys.path.append('../libsvm/python')
import numpy as np
from svmutil import *

name = {0:"Han", 1:"Jhow", 2:"Jing", 3:"Rick"}

def Training(data, params):
    param = '-s 2 -t 2 -n ' + str(params[0]) + ' -g ' + str(params[1])
    print param
    model = svm_train([1 for _ in range(len(data))], data.tolist(), param)

    p_label, p_acc, p_val = svm_predict([1 for _ in range(len(data))], data.tolist(), model)

    return model, np.max(p_val)

def Testing(modelPool, p_table, testingFeature, testingLabel=[]):
    pVal = -1
    for feature in testingFeature:
        idx = 0
        tmp = []
        for model in modelPool:
            p_label, _, p_val = svm_predict([1], [feature.tolist()], model)
            print p_val[0][0]
            tmp.append(p_val[0][0]/p_table[idx])
            idx += 1
        pVal = np.where(tmp == np.max(tmp))[0]

    return pVal
