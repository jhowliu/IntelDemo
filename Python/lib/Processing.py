import sys
sys.path.append('/home/jhowliu/Work/IntelDemo/Python/libsvm/python/')
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
    tmp_probs = np.array([])
    for feature in testingFeature:
        pVal = -1
        idx = 0
        tmp = []

        for (model, LogReg) in zip(modelPool, LogRegPool):
            p_label, _, p_val = svm_predict([1], [feature.tolist()], model)
            print p_val
            tmp_probs = np.insert(tmp_probs, tmp_probs.shape[0], LogReg.predict_proba(np.array(p_val))[0][1])
            tmp.append(p_val[0][0]/p_table[idx])
            idx += 1

        if np.sum(np.array(tmp) > 0) != 0:
            pVal = np.where(tmp == np.max(tmp))[0][0]

        if np.max(tmp_probs) > 0.5 and pVal == -1:
            tmp_probs[tmp_probs==np.max(tmp_probs)] -= 0.5
        print tmp_probs
        for x in tmp_probs.tolist():
            probs.append((str(np.around(x * 100, decimals=3)) + '%' , str(np.around(x / (np.sum(np.array(tmp_probs))) * 100, decimals=3)) + '%'))


        print pVal

    return pVal, probs
