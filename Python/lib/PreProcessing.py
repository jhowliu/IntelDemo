#-*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from MovingAvg import MovingAvg

def Preprocessing(rawSeries, n=2, maxLen=200):
    # Check for series size
    if len(rawSeries.shape) == 1:
        rawSeries = rawSeries.T

    '''
    # Delete peak value (More than 3 standard deviation)
    for idx in range(rawSeries.shape[1]-4):
        upper = np.mean(rawSeries[:, idx+1]) + 3*np.std(rawSeries[:, idx+1])
        lower = np.mean(rawSeries[:, idx+1]) - 3*np.std(rawSeries[:, idx+1])

        rawSeries[np.where(rawSeries[:, idx+1] > upper), idx+1] = upper
        rawSeries[np.where(rawSeries[:, idx+1] < lower), idx+1] = lower
    '''

    idx = np.where(rawSeries[:, 0] == 0)[0]
    idx = np.insert(idx, idx.shape[0], rawSeries.shape[0])
    dataLen = idx[1:]-idx[0:-1]

    # Remove the data which length is smaller than 100
    idx = idx[dataLen > 100]
    dataLen = dataLen[dataLen > 100]

    axis1  = np.zeros((idx.shape[0], maxLen))
    axis2  = np.zeros((idx.shape[0], maxLen))
    axis3  = np.zeros((idx.shape[0], maxLen))
    axis4  = np.zeros((idx.shape[0], maxLen))
    axis5  = np.zeros((idx.shape[0], maxLen))
    axis6  = np.zeros((idx.shape[0], maxLen))

    for i in range(idx.shape[0]):
        axis1[i, 0:dataLen[i]] = rawSeries[idx[i]:idx[i]+dataLen[i], 1]
        axis2[i, 0:dataLen[i]] = rawSeries[idx[i]:idx[i]+dataLen[i], 2]
        axis3[i, 0:dataLen[i]] = rawSeries[idx[i]:idx[i]+dataLen[i], 3]
        axis4[i, 0:dataLen[i]] = rawSeries[idx[i]:idx[i]+dataLen[i], 4]
        axis5[i, 0:dataLen[i]] = rawSeries[idx[i]:idx[i]+dataLen[i], 5]
        axis6[i, 0:dataLen[i]] = rawSeries[idx[i]:idx[i]+dataLen[i], 6]


    return axis1, axis2, axis3, axis4, axis5, axis6

# Testing Code
if __name__ == '__main__':
    Preprocessing(np.array([[0,1,2,3,4,5,6,7,8,9,10],[1,1,2,3,2,4,2,2,2,2,2], [3,1,2,3,2,2,2,2,2,2,2],[0,1,2,1,2,2,2,3,3,3,3],[1,2,2,2,1,1,2,3,4,5,6],[0,1,2,1,2,2,2,3,3,3,3],[1,2,2,2,1,1,2,3,4,5,6]]))
