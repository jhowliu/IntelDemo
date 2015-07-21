# -*- coding: utf-8 -*-
import serial
import os.path
import sys
sys.path.append('lib')
import random as rd
import numpy as np
from datetime import datetime
from Envelope import envelope
from Demo_UI import Base
from Processing import Testing
from Processing import Training
from Sampling import OverSampling
from Vectorization import Vectorize
from PreProcessing import Preprocessing
from sklearn.linear_model import LogisticRegression

def OpenSerial():
    return serial.Serial('/dev/tty.usbmodem1421', 9600)

def TrainingModel(dataPool, trainingLabel):
    params = [[0.000200000000000000, 0.0229746337890625], [0.0128000000000000, 0.000637500000000000], [0.00320000000000000, 0.00113906250000000], [0.00640000000000000,0.00170859375000000]]

    testingData = np.zeros((1, 96))
    testingLabel = []
    rangeOfData = [0]
    modelPool = []
    p_pool = []
    p_table = []
    LogRegPool = []

    # The flag of current person
    currentGuy = 0
    for data in dataPool:
        # Vectorization
        vectorFeature = np.zeros((data.shape[1], 1))
        # Combine vectorize features of all axis. (Dimension = n * 153)
        for x in data:
            vectorFeature = np.insert(vectorFeature, vectorFeature.shape[1], Vectorize(x), axis=1)
        vectorFeature = np.delete(vectorFeature, 0, axis=1)
        print vectorFeature.shape

        # Envelope
        '''
        for idx in range(5):
            tmp = []
            for i in range(4):
                tmp.extend(dataPool[i][idx].tolist())

            envelopeResult = np.array(envelope(np.array(trainingLabel[idx*len(tmp):(idx+1)*len(tmp)]), tmp, dataPool[currentGuy][idx], 1))
            vectorFeature = np.insert(vectorFeature, vectorFeature.shape[1], envelopeResult.T, axis=1)
        '''

        # Create testing lable
        testingLabel.extend([currentGuy for _ in xrange(vectorFeature.shape[0])])
        testingData = np.insert(testingData, testingData.shape[0], vectorFeature, 0)

        currentGuy +=1
        rangeOfData.append(rangeOfData[len(rangeOfData)-1] + data.shape[1])


    testingData = np.delete(testingData, 0, axis=0)

    for i in range(4):
        writeInFile(testingData[rangeOfData[i]:rangeOfData[i+1]], i)

    # Max-Min Normalize
    scaleRange = np.abs(np.max(testingData, 0) - np.min(testingData, 0))
    scaleMin = np.min(testingData, 0)
    # Max and Min is 0, avoiding to divide by zero
    scaleRange[scaleRange == 0] = 1
    testingData = (testingData - scaleMin)/scaleRange


    for i in range(len(dataPool)):
        # OverSampling
        label  = np.array([0 for _ in range(testingData.shape[0])])
        label[rangeOfData[i]:rangeOfData[i+1]] = 1
        sample = OverSampling(np.insert(testingData, testingData.shape[1], label, axis=1))
        model, p_val, p_vals = Training(testingData[rangeOfData[i]:rangeOfData[i+1]], sample, params[i])
        # Logistic Regression
        LogReg = LogisticRegression(C=1e3)
        LogReg.fit(np.array(p_vals), sample[:, -1])

        p_pool.append(p_val)
        p_table.append(p_vals)
        modelPool.append(model)
        LogRegPool.append(LogReg)

    print "Finish"
    return modelPool, p_pool, p_table, testingData, testingLabel, scaleRange, scaleMin, rangeOfData, LogRegPool

def DataRepresent(dataPool, trainingLabel, rawdata, scaleRange, scaleMin):
    # Preprocessing
    [axis1, _, axis3, axis4, axis5, axis6, press1, press2, press3, press4] = Preprocessing(rawdata, maxLen=250, n=5)
    testingData = np.array([axis1, axis3, axis4, axis5, axis6, press1, press2, press3, press4])

    testingFeature = np.zeros((testingData.shape[1], 1))
    # Vectorization
    for x in testingData:
        testingFeature = np.insert(testingFeature, testingFeature.shape[1], Vectorize(x), axis=1)

    testingFeature = np.delete(testingFeature, 0, axis=1)

    # Envelope
    for idx in range(9):
        tmp = []
        for i in range(4):
            tmp.extend(dataPool[i][idx].tolist())

        envelopeResult = np.array(envelope(np.array(trainingLabel[idx*len(tmp):(idx+1)*len(tmp)]), tmp, testingData[idx].tolist(), 1))
        testingFeature = np.insert(testingFeature, testingFeature.shape[1], envelopeResult.T, axis=1)

    # Max-min Normalize
    testingFeature = (testingFeature-scaleMin)/scaleRange

    return testingFeature

def LoadTrainingData(namelist):
    print namelist
    dataPool = []
    trainingLabel = []
    i = 0
    # Load the data in numpy's type
    for name in namelist:
        data = np.genfromtxt(name, delimiter=',')
        print data.shape
        # Do preprocessing & moving average
        [axis1, axis2, axis3, axis4, axis5, axis6] = Preprocessing(data, maxLen=250, n=5)

        cleanedData = np.array([axis1, axis2, axis3, axis4, axis5, axis6])

        # Collect data which has been processing
        dataPool.append(cleanedData)

        # Create training label
        trainingLabel.extend([i for _ in range(axis1.shape[0])])
        i+=1

    trainingLabel = trainingLabel * 6

    # Training Model
    modelPool, p_pool, p_table, testingData, _, scaleRange, scaleMin, rangeOfData, LogRegPool = TrainingModel(dataPool[:4], trainingLabel)
    return modelPool, p_pool, dataPool, trainingLabel, scaleRange, scaleMin, LogRegPool

def Train(namelist=['~/DataSet/Han.csv', '~/DataSet/jhow.csv', '~/DataSet/jing.csv', '~/DataSet/rick.csv']):
    modelPool, p_tabel, dataPool, trainingLabel, scaleRange, scaleMin, LogRegPool = LoadTrainingData(namelist)

    ## Use intruder data
    #data = np.genfromtxt(intruder, delimiter=',')
    #print data.shape
    ## Do preprocessing & moving average
    #testingFeature = DataRepresent(dataPool, trainingLabel, data, scaleRange, scaleMin)
    ## Random sampling
    #testingFeature = testingFeature[rd.sample(range(len(testingFeature)), 1), :]
    #print testingFeature.shape
    #Testing(LogRegPool, modelPool, p_tabel, testingFeature, [-1 for _ in range(len(testingFeature))])
    #print "finish"

    return modelPool, p_tabel, dataPool, trainingLabel, scaleRange, scaleMin, LogRegPool

def Run(namelist):
    modelPool, p_table, dataPool, trainingLabel, scaleRange, scaleMin, LogRegPool = Train(namelist)
    print "Ready"
    currentTime = datetime.now()
    #ser = OpenSerial()
    #line = ser.readline()
    #data = []

    #print line

    #line = ser.readline()
    #while line:
    #    print line

    #    line = line.strip()

    #    if (line != "Closed"):
    #        line = (line + ',14,' + str(currentTime.weekday()+1)).split(',')
    #        if len(line) != 13:
    #            pVal = -2
    #            probs =[]
    #        line = map(lambda x: int(x), line)
    #        data.extend([line])

    #    if (line == "Closed"):
    #        # Data representation
    #        if np.array(data).shape[0] > 192:
    #            data = (np.array(data)[:192, :]).tolist()
    #        if np.array(data).shape[1] == 13:
    #            testingFeature = DataRepresent(dataPool, trainingLabel, np.array(data), scaleRange, scaleMin)
    #            print testingFeature.shape
    #            pVal, probs = Testing(LogRegPool, modelPool, p_table, testingFeature, [1])
    #            base.predict(pVal, probs)
    #            data =[]
    #        else:
    #            # Do nothing
    #            pVal = -2
    #            probs =[]
    #            data = []

    #    line = ser.readline()

    #return pVal, probs

def writeInFile(data, param):
    #name = {0:'Han_feature', 1:'Jhow_feature', 2:'Jing_feature', 3:'Rick_feature'}
    name = {0:'arthur_features', 1:'brian_features', 2:'nofar_features', 3:'shalom_features'}
    out = open(name[param] + '.csv', 'w')
    for line in data.tolist():
        line = map(lambda x: str(x), line)
        out.write(','.join(line) + '\n')

    out.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: python ReadSerial.py <fileName>"
        exit(1)
    #base = Base()
    #base.start()
    Run([sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]])
