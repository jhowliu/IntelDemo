# -*- coding: utf-8 -*-
import serial
import os.path
import sys
from PreProcessing import PreProcessing 
from Vectorization import Vectorize
from datetime import datetime

def OpenSerial():
    return serial.Serial('/dev/ttyACM0', 9600)

def writeInFile(name, data):
    fileName = name + ".csv"
    currentTime = datetime.now()

    with open(fileName, 'a') as f:
        for tmp in data:
            f.write(tmp + "," + str(currentTime.hour) + "," + str(currentTime.weekday()+1) +  "\n")
def Run(name):
    # Load the data in numpy's type
    data = np.loadtxt(name, delimiter=',')
    # Do preprocessing & moving average
    [axis1, axis2, axis3, axis4, axis5, axis6, press1, press2, press3, press4] = PreProcessing(data)
    preproData = [axis1, axis2, axis3, axis4, axis5, axis6, press1, press2, press3, press4]
    # Vectorization
    vectorFeature = Vectorize(preproData)
    print "Finish"
def Read(name):
    ser = OpenSerial()
    line = ser.readline()
    dataList = []

    print line

    line = ser.readline()
    while line:
        print line

        line = line.strip()

        if (line != "Closed"):
            dataList.extend([line])

        if (line == "Closed"):
            writeInFile(name, dataList)
            print count
            # Run the Main function
            Run(name)
            count +=1
            dataList = []

        line = ser.readline()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: python ReadSerial.py <fileName>"
        exit(1)
    Read(sys.argv[1])
