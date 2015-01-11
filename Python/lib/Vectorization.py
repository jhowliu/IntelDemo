# -*- coding: utf-8 -*-
import numpy as np

def Vectorize(seriesData):
    # Check for series size
    if len(seriesData.shape) == 1:
        seriesData = seriesData.reshape(1, seriesData.shape[0])

    # Get length of series data 
    dataLength = seriesData.shape[0]

    # Feature space
    vectorFeature = np.zeros((dataLength, 16))

    # 1) to 3) min, max mean
    tsMin  = np.min(seriesData, 1)
    tsMax  = np.max(seriesData, 1)
    tsMean = np.mean(seriesData, 1)

    vectorFeature[:, 0] = tsMin
    vectorFeature[:, 1] = tsMax
    vectorFeature[:, 2] = tsMean

    # 4) and 5) number of Peaks and Valleys
    # 6) and 7) mean of peak and valley values
    # 8) and 9) mean of interval between peaks and valley

    # Find location of peak and valley, including start and end point
    velocityDiff = seriesData[:, 1:]-seriesData[:, 0:-1]
    velocityBool = np.ones(velocityDiff.shape)

    velocityBool[velocityDiff < 1] = -1

    trendDiff = velocityBool[:, 1:] + velocityBool[:, 0:-1]

    pivotIdx = np.where(trendDiff == 0)
    trendDirection = velocityBool[pivotIdx[0], pivotIdx[1] + 1]

    peakIdx   = np.array([pivotIdx[0][trendDirection < 0], pivotIdx[1][trendDirection < 0] + 1])
    valleyIdx = np.array([pivotIdx[0][trendDirection > 0], pivotIdx[1][trendDirection > 0] + 1])

    # Compute features of each sameple of time series
    for idx in range(len(seriesData)):
        curPeakIdx   = np.array([0, seriesData.shape[1]-1])
        curValleyIdx = np.array([0, seriesData.shape[1]-1])

        curPeakIdx = np.insert(curPeakIdx, 1, peakIdx[1][peakIdx[0] == idx])
        curValleyIdx = np.insert(curValleyIdx, 1, valleyIdx[1][valleyIdx[0] == idx])

        vectorFeature[idx, 3] = len(curPeakIdx)
        vectorFeature[idx, 4] = len(curValleyIdx)
        vectorFeature[idx, 5] = np.mean(seriesData[idx, curPeakIdx])
        vectorFeature[idx, 6] = np.mean(seriesData[idx, curValleyIdx])
        vectorFeature[idx, 7] = np.mean(curPeakIdx[1:] - curPeakIdx[0:-1])
        vectorFeature[idx, 8] = np.mean(curValleyIdx[1:] - curValleyIdx[0:-1])

    # 10) First reading of each time series
    # 11) Median of first 10% data points
    # 12) to 16) Mean of 5 equal parts of time series
    # 17) Sum of absolute value of changes in amplitude reading of timestamps

    vectorFeature[:, 9] = seriesData[:, 0]
    vectorFeature[:, 10] = np.median(seriesData[:, 0:np.floor(seriesData.shape[1] * 0.10)], 1)

    segLenth = float(len(seriesData[0])) / 5.0

    for idx in range(5):
        vectorFeature[:, 11+idx] = np.mean(seriesData[:, np.floor(segLenth * idx):np.floor(segLenth * (idx+1))], 1)

    #vectorFeature[:, 16] = np.sum(np.abs(velocityDiff))

    return vectorFeature.T


