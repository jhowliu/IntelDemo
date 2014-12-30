#Gk-*- coding: utf-8 -*-
import numpy as np
from MovingAvg import MovingAvg

def Preprocessing(rawSeries, n=2):

    print rawSeries.shape
    # Check for series size
    if len(rawSeries.shape) == 1:
        rawSeries = rawSeries.T

    # Delete peak value (More than 3 standard deviation)
    for idx in range(rawSeries.shape[1]-4):
        upper = np.mean(rawSeries[:, idx+1]) + 3*np.std(rawSeries[:, idx+1])
        lower = np.mean(rawSeries[:, idx+1]) - 3*np.std(rawSeries[:, idx+1])

        rawSeries[np.where(rawSeries[:, idx+1] > upper), idx+1] = upper
        rawSeries[np.where(rawSeries[:, idx+1] < lower), idx+1] = lower

    idx = np.where(rawSeries[:, 0] == 0)
    idx = np.insert(idx[0], idx[0].shape[0], rawSeries.shape[0])

    dataLen = idx[1:]-idx[0:-1]
    maxLen = np.max(dataLen)-n+1

    axis1  = np.zeros((idx.shape[0]-1, maxLen))
    axis2  = np.zeros((idx.shape[0]-1, maxLen))
    axis3  = np.zeros((idx.shape[0]-1, maxLen))
    axis4  = np.zeros((idx.shape[0]-1, maxLen))
    axis5  = np.zeros((idx.shape[0]-1, maxLen))
    axis6  = np.zeros((idx.shape[0]-1, maxLen))

    press1 = np.zeros((idx.shape[0]-1, maxLen))
    press2 = np.zeros((idx.shape[0]-1, maxLen))
    press3 = np.zeros((idx.shape[0]-1, maxLen))
    press4 = np.zeros((idx.shape[0]-1, maxLen))

    for i in range(idx.shape[0]-1):
        axis1[i, 0:dataLen[i]-n+1] = MovingAvg(rawSeries[idx[i]:idx[i]+dataLen[i], 1], n)
        axis2[i, 0:dataLen[i]-n+1] = MovingAvg(rawSeries[idx[i]:idx[i]+dataLen[i], 2], n)
        axis3[i, 0:dataLen[i]-n+1] = MovingAvg(rawSeries[idx[i]:idx[i]+dataLen[i], 3], n)
        axis4[i, 0:dataLen[i]-n+1] = MovingAvg(rawSeries[idx[i]:idx[i]+dataLen[i], 4], n)
        axis5[i, 0:dataLen[i]-n+1] = MovingAvg(rawSeries[idx[i]:idx[i]+dataLen[i], 5], n)
        axis6[i, 0:dataLen[i]-n+1] = MovingAvg(rawSeries[idx[i]:idx[i]+dataLen[i], 6], n)

        press1[i, 0:dataLen[i]-n+1] = MovingAvg(rawSeries[idx[i]:idx[i]+dataLen[i], 7], n)
        press2[i, 0:dataLen[i]-n+1] = MovingAvg(rawSeries[idx[i]:idx[i]+dataLen[i], 8], n)
        press3[i, 0:dataLen[i]-n+1] = MovingAvg(rawSeries[idx[i]:idx[i]+dataLen[i], 9], n)
        press4[i, 0:dataLen[i]-n+1] = MovingAvg(rawSeries[idx[i]:idx[i]+dataLen[i], 10], n)

    return axis1, axis2, axis3, axis4, axis5, axis6, press1, press2, press3, press4

# Testing Code
if __name__ == '__main__':
    Preprocessing(np.array([[0,1,2,3,4,5,6,7,8,9,10],[1,1,2,3,2,4,2,2,2,2,2], [3,1,2,3,2,2,2,2,2,2,2],[0,1,2,1,2,2,2,3,3,3,3],[1,2,2,2,1,1,2,3,4,5,6],[0,1,2,1,2,2,2,3,3,3,3],[1,2,2,2,1,1,2,3,4,5,6]]))
