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
    return serial.Serial('/dev/tty.usbmodem1421', 9600)

def TrainingModel(dataPool, trainingLabel):
    params = [[0.00160000000000000, 0.0129746337890625], [0.000400000000000000, 0.00256289062500000], [0.00320000000000000, 0.00384433593750000], [0.0256000000000000, 0.0291929260253906]]
    testingData = np.zeros((1, 252))
    testingLabel = []
    rangeOfData = [0]
    modelPool = []
    p_tabel = []

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

        testingData = np.insert(testingData, testingData.shape[0], vectorFeature, 0)
        # Seperate testing and training
        #allIdxSet  = set(range(len(data[0])))
        #testingIdxSet = set(rd.sample(range(len(data[0])), 40))

        #model, p_val = Training(vectorFeature[list(allIdxSet-testingIdxSet)], params[currentGuy])

        currentGuy +=1
        rangeOfData.append(rangeOfData[len(rangeOfData)-1] + data.shape[1])

    # Max-Min Normalize
    scaleRange = np.abs(np.max(testingData, 0) - np.min(testingData, 0))
    scaleMin = np.min(testingData, 0)
    # Max and Min is 0, avoiding to divide by zero
    scaleRange[scaleRange == 0] = 1
    testingData = (testingData - scaleMin)/scaleRange

    #print np.min(testingData[:153], 0)
    #print np.max(testingData[:153], 0)
    #print np.mean(testingData[:153], 0)
    for i in range(len(dataPool)):
        model, p_val = Training(testingData[rangeOfData[i]:rangeOfData[i+1]], params[i])

        modelPool.append(model)
        p_tabel.append(p_val)

    testingData = np.delete(testingData, 0, axis=0)
    print "Finish"
    return modelPool, p_tabel, testingData, testingLabel, scaleRange, scaleMin

def DataRepresent(dataPool, trainingLabel, rawdata, scaleRange, scaleMin):
    # Preprocessing
    [axis1, _, axis3, axis4, axis5, axis6, press1, press2, press3, press4] = Preprocessing(rawdata, maxLen=192, n=5)
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
        # Do preprocessing & moving average
        [axis1, _, axis3, axis4, axis5, axis6, press1, press2, press3, press4] = Preprocessing(data, maxLen=192, n=5)
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
    modelPool, p_tabel, _, _, scaleRange, scaleMin= TrainingModel(dataPool[:4], trainingLabel)

    # Get intruder data
    #testingFeature = TestingDataRepresent(dataPool[:4], trainingLabel, dataPool[4])
    # Append intruder lable on testingLabel
    #testingLabel.extend([-1 for _ in range(testingFeature.shape[0])])
    #vectorFeature = np.insert(vectorFeature, vectorFeature.shape[0], testingFeature, axis=0)
    # Testing 
    #Testing(modelPool, p_tabel, vectorFeature, testingLabel)
    return modelPool, p_tabel, dataPool, trainingLabel, scaleRange, scaleMin

def Run(namelist=['~/DataSet/Han.csv', '~/DataSet/jhow.csv', '~/DataSet/jing.csv', '~/DataSet/rick.csv'], intruder='~/DataSet/Intruder.csv'):
    modelPool, p_tabel, dataPool, trainingLabel, scaleRange, scaleMin = LoadTrainingData(namelist)
    currentTime = datetime.now()

    # Use intruder data
    data = np.genfromtxt(intruder, delimiter=',')
    print data.shape
    # Do preprocessing & moving average
    testingFeature = DataRepresent(dataPool, trainingLabel, data, scaleRange, scaleMin)
    # Random sampling
    testingFeature = testingFeature[rd.sample(range(len(testingFeature)), 10), :]
    print testingFeature.shape
    Testing(modelPool, p_tabel, testingFeature, [-1 for _ in range(len(testingFeature))])
    ser = OpenSerial()
    line = ser.readline()
    data = []

    print line

    line = ser.readline()
    while line:
        print line

        line = line.strip()

        if (line != "Closed"):
            line = (line + ',14,' + str(currentTime.weekday()+1)).split(',')
            line = map(lambda x: int(x), line)
            data.extend([line])

        if (line == "Closed"):
            # Data representation
            testingFeature = DataRepresent(dataPool, trainingLabel, np.array(data), scaleRange, scaleMin)
            print testingFeature.shape
            pVal = Testing(modelPool, p_tabel, testingFeature, [1])
            print pVal
            data = []

        line = ser.readline()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: python ReadSerial.py <fileName>"
        exit(1)
    Run([sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]], sys.argv[5])
