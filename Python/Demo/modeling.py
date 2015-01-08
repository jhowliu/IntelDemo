import sys
import numpy as np
sys.path.append('../')
sys.path.append('../../SSVM')
from Setup import Load
from sklearn import svm
from Sampling import OverSampling
#from predictor import Predictor
#from trainer import Trainer

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
    print OverSampling(trainingFeatures).shape
    #trainer = Trainer(trainingFeatures, trainingFeatures.shape[1]-1)

def Start():
    trainingFeatures, dataIdx, trainingLabel = Load()
    AxisVectorFeature, PressVectorFeature, AxisEnvelopeFeature, PressEnvelopeFeature = SplitFeatures(trainingFeatures, dataIdx)
    for feature in [AxisVectorFeature, PressVectorFeature, AxisEnvelopeFeature, PressEnvelopeFeature]:
        for currentGuy in range(4):
            trainingLabel = np.array([0 for _ in range(feature.shape[0])])
            trainingLabel[dataIdx[currentGuy]:dataIdx[currentGuy+1]] = 1
            Training(feature, trainingLabel)

if __name__ == '__main__':
    Start()
