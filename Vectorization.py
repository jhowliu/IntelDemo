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

    vectorFeature[:, 1] = tsMin
    vectorFeature[:, 2] = tsMax
    vectorFeature[:, 3] = tsMean

    # 4) and 5) number of Peaks and Valleys
    velocityDiff = seriesData[:, 1:]-seriesData[:, 0:-1]
    velocityBool = ones(velocityDiff.shape)

    velocityBool[velocityDiff < 1] = -1

    trendDirect = velocityBool[:, 1:] - velocityBool[:, 0:-1]


