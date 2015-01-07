import sys
import numpy as np
sys.path.append('../../SSVM')
from Setup import Run
from predictor import Predictor
from trainer import Trainer
from sklearn import svm

# Training model with (1 vs rest) multiclassification. (4 models)
def SplitFeatures(trainingFeatures, dataIdx):
    trainingFeatures = np.array(trainingFeatures)
    # Axis  features (Vectorize)
    AxisVectorFeature    = trainingFeatures[:, :80]
    # Press features (Vectorize)
    PressVectorFeature   = trainingFeatures[:, 80:144]
    # Axis  features (Envelope)
    AxisEnvelopeFeature  = trainingFeatures[:, 144:204]
    # Press features (Envelope)
    PressEnvelopeFeature = trainingFeatures[:, 204:]

    return AxisVectorFeature, PressVectorFeature, AxisEnvelopeFeature, PressEnvelopeFeature

def Training(trainingFeatures, trainingLabel):
    trainingFeatures = np.insert(trainingFeatures, trainingFeatures.shape[1], trainingLabel, axis=1)
    print trainingFeatures.shape

def Start():
    trainingFeatures, dataIdx = Run()
    AxisVectorFeature, PressVectorFeature, AxisEnvelopeFeature, PressEnvelopeFeature = SplitFeatures(trainingFeatures, dataIdx)
    for feature in [AxisVectorFeature, PressVectorFeature, AxisEnvelopeFeature, PressEnvelopeFeature]:
        for currentGuy in range(4):
            trainingLabel = np.array([0 for _ in range(feature.shape[0])])
            trainingLabel[dataIdx[currentGuy]:dataIdx[currentGuy+1]] = 1
            Training(feature, trainingLabel)

if __name__ == '__main__':
    Start()
