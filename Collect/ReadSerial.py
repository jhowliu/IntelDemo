import serial
import os.path
import sys
from datetime import datetime

def OpenSerial():
    return serial.Serial('/dev/ttyACM0', 9600)

def writeInFile(name, data):
    fileName = name + ".csv"
    currentTime = datetime.now()

    with open(fileName, 'a') as f:
        for tmp in data:
            f.write(tmp + "," + str(currentTime.hour) + "," + str(currentTime.weekday()+1) +  "\n")

def Run(name, count):
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
            count +=1
            dataList = []

        line = ser.readline()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Usage: python ReadSerial.py <fileName> <counter>"
        exit(1)
    Run(sys.argv[1], int(sys.argv[2]))
