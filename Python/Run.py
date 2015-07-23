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
from Processing import Evalidation
from Processing import Testing
from Processing import Training
from PreProcessing import Preprocessing
from sklearn.linear_model import LogisticRegression

def OpenSerial():
    return serial.Serial('/dev/tty.usbmodem1421', 9600)

def TrainingModel(dataPool, trainingLabel):
    labels = []

    # The flag of current person
    i = 0
    # Create a feature for each one class
    features = np.zeros((1, 72))
    print features.shape

    for data in dataPool:
        # Use to concat all axies data
        tmp = np.zeros((data.shape[1], 1))
        # Create an envelope features
        for idx in range(6):
            training_sample = []
            map(lambda i: training_sample.extend(dataPool[i][idx].tolist()), xrange(4))
            # We have 4 labels, so we will get a vector which size is 12 for each axis
            envelopeResult = np.array(envelope(np.array(trainingLabel[idx*len(training_sample):(idx+1)*len(training_sample)]), training_sample, dataPool[i][idx], 1))

            tmp = np.insert(tmp, tmp.shape[1], envelopeResult.T, axis=1)

        tmp = np.delete(tmp, 0, axis=1)

        print tmp.shape

        features = np.insert(features, features.shape[0], tmp, axis=0)

        # Create testing lable
        labels.extend([i for _ in xrange(tmp.shape[0])])

        i = i+1
    # Remove the first row of zeros 
    features = np.delete(features, 0, axis=0)

    print np.array(features).shape, np.array(labels).shape

    model = Training(features, labels, c=10**-5)
    Evalidation(features, np.array(labels))
    '''
    # For saving the features
    for i in range(4):
        writeInFile(testingData[rangeOfData[i]:rangeOfData[i+1]], i)
    '''

    print model
    print "Finish"

    return model

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
    print testingFeature
    testingFeature = np.delete(testingFeature, 0, axis=1)

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
    model = TrainingModel(dataPool[:4], trainingLabel)
    return model, dataPool, trainingLabel

def Train(namelist=['~/DataSet/Han.csv', '~/DataSet/jhow.csv', '~/DataSet/jing.csv', '~/DataSet/rick.csv']):
    model, dataPool, trainingLabel = LoadTrainingData(namelist)

    return model, dataPool, trainingLabel

def Run(namelist):
    model, dataPool, trainingLabel = Train(namelist)
    print "Ready"


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

    namelist = [sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]]
    test_data = np.genfromtxt(sys.argv[5], delimiter=',')

    model, dataPool, trainingLabel = Train(namelist)
    test_feature = DataRepresent(dataPool, trainingLabel, np.array(test_data))
    predicted_label = Testing(model, test_feature)

    print predicted_label
