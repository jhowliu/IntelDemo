# -*- coding: utf-8 -*-
import serial
import os.path
import sys
import numpy as np
from Training import Training
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

def TrainingModel(namelist):
    dataPool = []
    modelPool = []
    p_tabel = []
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
        trainingLabel.extend([i for _ in range(axis1.shape[0])])
        i+=1

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
            print len(tmp)
        #print envelopeResult



        model, p_val = Training(vectorFeature)

        modelPool.append(model)
        p_tabel.append(p_val)

    print "Finish"

def Read(name):
    TrainingModel(name)
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
    Read([sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]])
