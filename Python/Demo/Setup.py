import sys
sys.path.append('../')
from PreProcessing import Preprocessing
from Vectorization import Vectorize
from Envelope import envelope
from sklearn import svm
import numpy as np

def Loading(names):
    trainingLabel = []
    dataSet = []
    dataIdx = [0]
    idx = 0

    for name in names:
        data = np.genfromtxt(name, delimiter=',')
        a1, a2, a3, a4, a5, a6, p1, p2, p3, p4 = Preprocessing(data, n=5, maxLen=192)
        dataSet.append(np.array([a1, a3, a4, a5, a6, p1, p2, p3, p4]))
        dataIdx.append(dataIdx[idx] + len(a1))
        trainingLabel.extend([idx for _ in range(len(a1))])
        print a1.shape
        idx += 1

    trainingLabel = trainingLabel * 9

    print dataIdx

    return dataSet, dataIdx, trainingLabel

def DataRepresent(dataSet, trainingLabel):
    trainingFeatures = np.zeros((1, 252))
    # Vectorization
    CurrentGuy = 0
    for data in dataSet:
        vectorFeatures = np.zeros((data.shape[1], 1))
        # 9 axis
        for x in data:
            vectorFeatures = np.insert(vectorFeatures, vectorFeatures.shape[1], Vectorize(x), axis=1)

        # Envelope
        for idx in range(9):
            tmp = []
            for i in range(4):
                tmp.extend(dataSet[i][idx].tolist())

            envelopeResult = np.array(envelope(np.array(trainingLabel[idx*len(tmp):(idx+1)*len(tmp)]), tmp, dataSet[CurrentGuy][idx], 1))
            vectorFeatures = np.insert(vectorFeatures, vectorFeatures.shape[1], envelopeResult.T, axis=1)

        vectorFeatures = np.delete(vectorFeatures, 0, axis=1)

        trainingFeatures = np.insert(trainingFeatures, trainingFeatures.shape[0], vectorFeatures, 0)

        CurrentGuy += 1

    trainingFeatures = np.delete(trainingFeatures, 0, axis=0)

    return trainingFeatures

def Run():
    dataSet, dataIdx, trainingLabel = Loading(['../../Data/Han.csv', '../../Data/Jhow.csv', '../../Data/Jing.csv', '../../Data/Rick.csv'])
    trainingFeatures = DataRepresent(dataSet, trainingLabel)

    return trainingFeatures, dataIdx


if __name__ == '__main__':
    Run()
