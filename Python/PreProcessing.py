# -*- coding: utf-8 -*-
import numpy as np
import MovingAvg as mvavg

def Preprocessing(rawSeries):
    # Check for series size
    if len(rawSeries.shape) == 1:
        rawSeries = rawSeries.reshape(1, rawSeries.shape[0])

    idx = np.where(rawSeries[:, 0] == 0)
    idx = np.insert(idx[0], idx[0].shape[0], rawSeries.shape[0])

    dataLen = idx[1:]-idx[0:-1]
    maxLen = np.max(dataLen)

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
        axis1[i, 0:dataLen[i]] = rawSeries[idx[i]:idx[i]+dataLen[i], 1]
        axis2[i, 0:dataLen[i]] = rawSeries[idx[i]:idx[i]+dataLen[i], 2]
        axis3[i, 0:dataLen[i]] = rawSeries[idx[i]:idx[i]+dataLen[i], 3]
        axis4[i, 0:dataLen[i]] = rawSeries[idx[i]:idx[i]+dataLen[i], 4]
        axis5[i, 0:dataLen[i]] = rawSeries[idx[i]:idx[i]+dataLen[i], 5]
        axis6[i, 0:dataLen[i]] = rawSeries[idx[i]:idx[i]+dataLen[i], 6]

        press1[i, 0:dataLen[i]] = rawSeries[idx[i]:idx[i]+dataLen[i], 7]
        press2[i, 0:dataLen[i]] = rawSeries[idx[i]:idx[i]+dataLen[i], 8]
        press3[i, 0:dataLen[i]] = rawSeries[idx[i]:idx[i]+dataLen[i], 9]
        press4[i, 0:dataLen[i]] = rawSeries[idx[i]:idx[i]+dataLen[i], 10]


if __name__ == '__main__':
    Preprocessing(np.array([[0,1,2,3,4,5,6,7,8,9,10],[1,1,2,3,2,4,2,2,2,2,2], [3,1,2,3,2,2,2,2,2,2,2],[0,1,2,1,2,2,2,3,3,3,3],[1,2,2,2,1,1,2,3,4,5,6]]))
