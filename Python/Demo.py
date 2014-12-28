# -*- coding: utf-8 -*-
import serial
import os.path
import sys
import numpy as np
from PreProcessing import Preprocessing 
from Vectorization import Vectorize
from datetime import datetime

def OpenSerial():
    return serial.Serial('/dev/ttyACM0', 9600)

def writeInFile(name, data):
    fileName = name
    currentTime = datetime.now()

    with open(fileName, 'w') as f:
        for tmp in data:
            f.write(tmp + "," + str(currentTime.hour) + "," + str(currentTime.weekday()+1) +  "\n")
def Run(name):
    # Load the data in numpy's type
    data = np.genfromtxt(name, delimiter=',')
    # Do preprocessing & moving average
    [axis1, axis2, axis3, axis4, axis5, axis6, press1, press2, press3, press4] = Preprocessing(data)
    preproData = np.array([axis1, axis2, axis3, axis4, axis5, axis6, press1, press2, press3, press4])

    # Vectorization
    vectorFeature = np.zeros((preproData.shape[1], 1))

    # Combine vectorize features of all attribute. (Dimension = n * 170)
    for x in preproData:
        vectorFeature = np.insert(vectorFeature, vectorFeature.shape[1], Vectorize(x), axis=1)

    vectorFeature = np.delete(vectorFeature, 0, axis=1)

    print "Finish"

def Read(name):
    Run(name)
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
    Read(sys.argv[1])
