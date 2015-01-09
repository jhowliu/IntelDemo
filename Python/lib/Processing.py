import sys
sys.path.append('../libsvm/python')
import numpy as np
from svmutil import *

name = {0:"Han", 1:"Jhow", 2:"Jing", 3:"Rick"}

def Training(data, testing, params):
    param = '-s 2 -t 2 -n ' + str(params[0]) + ' -g ' + str(params[1])
    model = svm_train([1 for _ in range(len(data))], data.tolist(), param)
    p_label, p_acc, p_val = svm_predict(testing[:,-1].tolist(), testing[:, :-1].tolist(), model)

    return model, np.max(p_val), p_val

def Testing(LogRegPool, modelPool, p_table, testingFeature, testingLabel=[]):
    probs = []
    for feature in testingFeature:
        pVal = -1
        idx = 0
        tmp = []
        tmp_probs = []

        for (model, LogReg) in zip(modelPool, LogRegPool):
            p_label, _, p_val = svm_predict([1], [feature.tolist()], model)
            tmp_probs.append(LogReg.predict_proba(np.array(p_val))[0][1])
            tmp.append(p_val[0][0]/p_table[idx])
            idx += 1

        for x in tmp_probs:
            probs.append((str(np.around(x * 100, decimals=3)) + '%' , str(np.around(x / (np.sum(np.array(tmp_probs))) * 100, decimals=3)) + '%'))

        #print np.array(tmp)>0
        if np.sum(np.array(tmp) > 0) != 0:
            pVal = np.where(tmp == np.max(tmp))[0][0]

        print pVal

    return pVal, probs
