# -*- coding: utf-8 -*-
import sys
import numpy as np

def Vectorize(seriesData):
    # Get length of series data
    dataLength = len(seriesData)
    # Feature space
    vectorFeature = np.zeros((dataLength, 17))

    # 1) to 3) min, max mean
    tsMin  = np.min(seriesData, 1)
    tsMax  = np.min(seriesData, 1)
    tsMean = np.mean(seriesData, 1)

    vectorFeature[:, 0] = tsMin
    vectorFeature[:, 1] = tsMax
    vectorFeature[:, 2] = tsMean

    # 4) and 5) number of Peaks and Valleys
    # 6) and 7) mean of peak and valley values
    # 8) and 9) mean of interval between peaks and valley

    # Find location of peak and valley, including start and end point
    velocityDiff = seriesData[:, 1:]-seriesData[:, 0:-1]
    velocityBool = ones(velocityDiff.shape)

    velocityBool[velocityDiff < 1] = -1

    trendDiff = velocityBool[:, 1:] + velocityBool[:, 0:-1]

    pivotIdx = np.where(trendDiff == 0)

    trendDirection = velocityBool[pivotIdx[0], pivotIdx[1] + 1]

    peakIdx   = np.array(pivotIdx[0][trendDirection < 0], pivotIdx[1][trendDirection < 0] + 1)
    valleyIdx = np.array(pivotIdx[0][trendDirection > 0], pivotIdx[1][trendDirection > 0] + 1)

    # Compute features of each sameple of time series
    for idx in range(len(seriesData)):
        curPeakIdx   = np.array([0, seriesData.shape[1]])
        curValleyIdx = np.array([0, seriesData.shape[1]])

        curPeakIdx = np.insert(curPeakIdx, 1, peakIdx[1][peakIdx[0] == idx]
        curValleyIdx = np.insert(curValleyIdx, 1, valleyIdx[1][valleyIdx[0] == idx]

        vectorFeature[i, 3] = len(curPeakIdx)
        vectorFeature[i, 4] = len(curValleyIdx)
        vectorFeature[i, 5] = np.mean(seriesData[i, curPeakIdx])
        vectorFeature[i, 6] = np.mean(seriesData[i, curValleyIdx])
        vectorFeature[i, 7] = np.mean(curPeakIdx[1:] - curPeakIdx[0:-1])
        vectorFeature[i, 8] = np.mean(curValleyIdx[1:] - curValleyIdx[0:-1])

    # 10) First reading of each time series
    # 11) Median of first 10% data points
    # 12) to 16) Mean of 5 equal parts of time series
    # 17) Sum of absolute value of changes in amplitude reading of timestamps

    vectorFeature[:, 9] = seriesData[:, 0]
    vectorFeature[:, 10] = np.median(seriesData[:, 1:np.floor(seriesData.shape[1] * 0.10)], 1)

    segLenth = float(dataLength) / 5.0

    for idx in range(5):
        vectorFeature[:, 11+idx] = np.mean(seriesData[:, np.floor(segLenth * idx):np.floor(segLenth * (idx+1))], 1)

    vectorFeature[:, 16] = np.sum(np.abs(velocityDiff))
