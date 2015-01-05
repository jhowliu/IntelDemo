import sys
sys.path.append('../')
from PreProcessing import Preprocessing
from Vectorization import Vectorize
from sklearn import svm
import numpy as np

def Loading(names):
    dataSet = []
    dataIdx = [0]
    idx = 0

    for name in names:
        data = np.genfromtxt(name, delimiter=',')
        a1, a2, a3, a4, a5, a6, p1, p2, p3, p4 = Preprocessing(data, n=5, maxLen=192)
        dataSet.append(np.array([a1, a3, a4, a5, a6, p1, p2, p3, p4]))
        dataIdx.append(dataIdx[idx] + len(a1))
        idx += 1

    print dataIdx

    return dataSet, dataIdx


if __name__ == '__main__':
    Loading(['../../Data/Han.csv', '../../Data/jhow.csv', '../../Data/jing.csv', '../../Data/rick.csv'])
