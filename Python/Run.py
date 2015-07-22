# -*- coding: utf-8 -*-
import serial
import os.path
import sys
sys.path.append('lib')
import random as rd
import numpy as np
import pandas as pd
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
    params = [[0.000200000000000000, 0.0229746337890625], [0.0128000000000000, 0.00637500000000000], [0.00320000000000000, 0.00113906250000000], [0.00640000000000000,0.00170859375000000]]
    # The size of envelope
    testingData = np.zeros((1, 72))
    testingLabel = []
    rangeOfData = [0]
    modelPool = []
    p_pool = []
    p_table = []
    LogRegPool = []

    # The flag of current person
    currentGuy = 0
    # Create a feature for each one class
    for data in dataPool:
        vectorFeature = np.zeros((data.shape[1], 1))

        training_sample = []
        print np.array(training_sample).shape 
        # Envelope
        for idx in range(6):
            training_sample = []
            map(lambda i: training_sample.extend(dataPool[i][idx].tolist()), xrange(4))
            # We have 4 labels, so we will get a vector which size is 12 for each axis
            envelopeResult = np.array(envelope(np.array(trainingLabel[idx*len(training_sample):(idx+1)*len(training_sample)]), training_sample, dataPool[currentGuy][idx], 1))

            vectorFeature = np.insert(vectorFeature, vectorFeature.shape[1], envelopeResult.T, axis=1)

        vectorFeature = np.delete(vectorFeature, 0, axis=1)

        # Create testing lable
        testingLabel.extend([currentGuy for _ in xrange(vectorFeature.shape[0])])
        testingData = np.insert(testingData, testingData.shape[0], vectorFeature, 0)

        currentGuy +=1
        rangeOfData.append(rangeOfData[len(rangeOfData)-1] + data.shape[1])

    testingData = np.delete(testingData, 0, axis=0)

    '''
    for i in range(4):
        writeInFile(testingData[rangeOfData[i]:rangeOfData[i+1]], i)
    '''

    # Train a model and validation
    for i in range(len(dataPool)):
        # Create testing data
        label  = np.array([0 for _ in range(testingData.shape[0])])
        label[rangeOfData[i]:rangeOfData[i+1]] = 1
        sample = np.insert(testingData, testingData.shape[1], label, axis=1)
        model, p_val, p_vals = Training(testingData[rangeOfData[i]:rangeOfData[i+1]], sample, params[i])
        # Logistic Regression
        LogReg = LogisticRegression(C=1e3)
        LogReg.fit(np.array(p_vals), sample[:, -1])

        p_pool.append(p_val)
        p_table.append(p_vals)
        modelPool.append(model)
        LogRegPool.append(LogReg)

    print "Finish"
    return modelPool, p_pool, p_table, testingData, testingLabel, rangeOfData, LogRegPool

def DataRepresent(dataPool, trainingLabel, rawdata):
    # Preprocessing
    [axis1, axis2, axis3, axis4, axis5, axis6] = Preprocessing(rawdata, maxLen=250, n=5)
    testingData = np.array([axis1, axis2, axis3, axis4, axis5, axis6])
    #print testingData

    testingFeature = np.zeros((testingData.shape[1], 1))

    # Envelope
    for idx in range(6):
        training_sample = []
        map(lambda i: training_sample.extend(dataPool[i][idx].tolist()), xrange(4))

        envelopeResult = np.array(envelope(np.array(trainingLabel[idx*len(training_sample):(idx+1)*len(training_sample)]), training_sample, testingData[idx].tolist(), 1))
        testingFeature = np.insert(testingFeature, testingFeature.shape[1], envelopeResult.T, axis=1)

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
    modelPool, p_pool, p_table, testingData, _, rangeOfData, LogRegPool = TrainingModel(dataPool[:4], trainingLabel)
    return modelPool, p_pool, dataPool, trainingLabel, LogRegPool

def Train(namelist=['~/DataSet/Han.csv', '~/DataSet/jhow.csv', '~/DataSet/jing.csv', '~/DataSet/rick.csv']):
    modelPool, p_tabel, dataPool, trainingLabel, LogRegPool = LoadTrainingData(namelist)

    return modelPool, p_tabel, dataPool, trainingLabel, LogRegPool

def Run(namelist):
    modelPool, p_table, dataPool, trainingLabel, LogRegPool = Train(namelist)
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
    #            testingFeature = DataRepresent(dataPool, trainingLabel, np.array(data))
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
    namelist = [sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]]
    test_data = np.genfromtxt(sys.argv[5], delimiter=',')
    modelPool, p_table, dataPool, trainingLabel, LogRegPool = Train(namelist)
    testingFeature = DataRepresent(dataPool, trainingLabel, np.array(test_data))
    pVal, probs = Testing(LogRegPool, modelPool, p_table, testingFeature, [1])
    print probs
