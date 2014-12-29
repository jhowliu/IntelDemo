# -*- coding: utf-8 -*-
import serial
import os.path
import sys
import random as rd
import numpy as np
from Processing import Training
from Processing import Testing
from PreProcessing import Preprocessing
from Vectorization import Vectorize
from Envelope import envelope
from datetime import datetime

def OpenSerial():
    return serial.Serial('/dev/ttyACM0', 9600)

def TrainingModel(dataPool, trainingLabel):
    params = [[0.00160000000000000, 0.0129746337890625], [0.000400000000000000, 0.00256289062500000], [0.00320000000000000, 0.00384433593750000], [0.0256000000000000, 0.0291929260253906]]
    modelPool = []
    p_tabel = []
    testingLabel = []
    testingData = np.zeros((1, 261))

    # The flag of current person
    currentGuy = 0
    for data in dataPool:
        # Vectorization
        vectorFeature = np.zeros((data.shape[1], 1))
        # Combine vectorize features of all attribute. (Dimension = n * 153)
        for x in data:
            vectorFeature = np.insert(vectorFeature, vectorFeature.shape[1], Vectorize(x), axis=1)
        vectorFeature = np.delete(vectorFeature, 0, axis=1)
        # Envelope
        for idx in range(9):
            tmp = []
            for i in range(4):
                tmp.extend(dataPool[i][idx].tolist())

            envelopeResult = np.array(envelope(np.array(trainingLabel[idx*len(tmp):(idx+1)*len(tmp)]), tmp, dataPool[currentGuy][idx], 1))
            vectorFeature = np.insert(vectorFeature, vectorFeature.shape[1], envelopeResult.T, axis=1)

        # Create testing lable
        testingLabel.extend([currentGuy for _ in range(40)])

        # Max-min Normalize
        scaleRange = np.abs(np.max(vectorFeature, 0) - np.min(vectorFeature, 0))
        # Max and Min is 0, avoiding to divide by zero
        scaleRange[scaleRange == 0] = 1
        vectorFeature = vectorFeature/scaleRange
        # Seperate testing and training
        #allIdxSet  = set(range(len(data[0])))
        #testingIdxSet = set(rd.sample(range(len(data[0])), 40))
        #testingData = np.insert(testingData, testingData.shape[0], vectorFeature[list(testingIdxSet)], 0)

        #model, p_val = Training(vectorFeature[list(allIdxSet-testingIdxSet)], params[currentGuy])
        model, p_val = Training(vectorFeature, params[currentGuy])

        modelPool.append(model)
        p_tabel.append(p_val)

        currentGuy +=1

    testingData = np.delete(testingData, 0, axis=0)

    print "Finish"
    return modelPool, p_tabel, testingData, testingLabel

def DataRepresent(dataPool, trainingLabel, rawdata):
    # Preprocessing
    [axis1, _, axis3, axis4, axis5, axis6, press1, press2, press3, press4] = Preprocessing(rawdata)
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
        testingFeature = np.insert(testingFeature, testingFeature.shape[1], (envelopeResult/176.).T, axis=1)

    # Max-min Normalize
    scaleRange = np.abs(np.max(testingFeature, 0) - np.min(testingFeature, 0))
    # Max and Min is 0, avoiding to divide by zero
    scaleRange[scaleRange == 0] = 1
    testingFeature = testingFeature/scaleRange

    return testingFeature

def LoadTrainingData(namelist):
    dataPool = []
    trainingLabel = []
    i = 0
    # Load the data in numpy's type
    for name in namelist:
        data = np.genfromtxt(name, delimiter=',')
        # Do preprocessing & moving average
        [axis1, _, axis3, axis4, axis5, axis6, press1, press2, press3, press4] = Preprocessing(data)
        preproData = np.array([axis1, axis3, axis4, axis5, axis6, press1, press2, press3, press4])
        # Collect data which has been processing
        dataPool.append(preproData)
        # Create training label
        print axis1.shape
        if i != 4:
            trainingLabel.extend([i for _ in range(axis1.shape[0])])
        i+=1

    trainingLabel = trainingLabel * 9

    # Training Model
    modelPool, p_tabel, _, _ = TrainingModel(dataPool[:4], trainingLabel)

    # Get intruder data
    #testingFeature = TestingDataRepresent(dataPool[:4], trainingLabel, dataPool[4])
    # Append intruder lable on testingLabel
    #testingLabel.extend([-1 for _ in range(testingFeature.shape[0])])
    #vectorFeature = np.insert(vectorFeature, vectorFeature.shape[0], testingFeature, axis=0)
    # Testing 
    #Testing(modelPool, p_tabel, vectorFeature, testingLabel)
    return modelPool, p_tabel, dataPool

def Run(namelist):
    modelPool, p_tabel, dataPool = LoadTrainingData(namelist)
    ser = OpenSerial()
    line = ser.readline()
    data = []

    print line

    line = ser.readline()
    while line:
        print line

        line = line.strip()

        if (line != "Closed"):
            data.extend([line])

        if (line == "Closed"):
            # Data representation
            testingFeature = DataRepresent(dataPool, trainingLabel, data)
            Testing(modelPool, p_tabel, testingFeature)
            data = []

        line = ser.readline()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: python ReadSerial.py <fileName>"
        exit(1)
    Run([sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]])
