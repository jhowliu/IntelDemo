# -*- coding: utf-8 -*-
import serial
import os.path
import sys
import numpy as np
from Processing import Training
from Processing import Testing
from PreProcessing import Preprocessing
from Vectorization import Vectorize
from Envelope import envelope
from datetime import datetime

def OpenSerial():
    return serial.Serial('/dev/ttyACM0', 9600)

def writeInFile(name, data):
    fileName = name
    currentTime = datetime.now()

    with open(fileName, 'w') as f:
        for tmp in data:
            f.write(tmp + "," + str(currentTime.hour) + "," + str(currentTime.weekday()+1) +  "\n")

def TrainingModel(dataPool, trainingLabel, testData):
    params = [[0.00160000000000000, 0.0129746337890625], [0.000400000000000000, 0.00256289062500000], [0.00320000000000000, 0.00384433593750000], [0.0256000000000000, 0.0291929260253906]]
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

        # Max-min Normalize
        scaleRange = np.abs(np.max(vectorFeature, 0) - np.min(vectorFeature, 0))
        # Max and Min is 0, avoiding to divide by zero
        scaleRange[scaleRange == 0] = 1
        vectorFeature = vectorFeature/scaleRange
        model, p_val = Training(vectorFeature, params[currentGuy])

        modelPool.append(model)
        p_tabel.append(p_val)

        currentGuy +=1

    print "Finish"
    return modelPool, p_tabel

def TestingDataRepresent(dataPool, trainingLabel, testingData):
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

def Read(namelist):
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

    modelPool, p_tabel = TrainingModel(dataPool[:4], trainingLabel, dataPool[4])
    testingFeature = TestingDataRepresent(dataPool[:4], trainingLabel, dataPool[4])
    Testing(modelPool, p_tabel, testingFeature)
    #ser = OpenSerial()
    #line = ser.readline()
    #dataList = []

    #print line

    #line = ser.readline()
    #while line:
    #    print line

    #    line = line.strip()

    #    if (line != "Closed"):
    #        dataList.extend([line])

    #    if (line == "Closed"):
    #        writeInFile(name, dataList)
    #        # Run the Main function
    #        Run(name)
    #        dataList = []

    #    line = ser.readline()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: python ReadSerial.py <fileName>"
        exit(1)
    Read([sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]])
