# -*- coding: utf-8 -*-
import numpy as np

# Input is a same length series
def MovingAvg(series, n=5):
    # Check for series size. (Example: array([1,2,3])
    if len(series.shape) == 1:
        series = series.reshape(1, series.shape[0])
    result = np.zeros((series.shape[0], series.shape[1]- n + 1))

    for idx in range(series.shape[1] - n + 1):
        result[:, idx] = np.mean(series[:, idx:idx+n], 1)

    return result

# Testing Code
if __name__ == '__main__':
    MovingAvg(np.array([[1,2,3,4,5,4,3,2,1], [5,4,3,2,1,2,3,4,5]]), 3)
