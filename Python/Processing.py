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

    p_val = np.array(p_val).reshape(1, len(p_val)).tolist()[0]

    return model, p_val

def Testing(modelPool, p_table, testingFeature, testingLabel=[]):
    #idx = 0
    for model in modelPool:
        p_label, _, p_val = svm_predict([1 for _ in range(len(testingFeature))], testingFeature.tolist(), model)
    #    print "No." + str(idx+1) + ": " + name[idx] + "'s Model"
    #    print str(np.sum(np.array(testingLabel)[np.array(p_label) == 1] == idx)) + "/40 " + str(np.sum(np.array(testingLabel)[np.array(p_label)==1] == idx) / 40.)
    #    idx +=1
