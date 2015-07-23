import sys
import numpy as np
from sklearn import cross_validation
from sklearn.svm import LinearSVC

name = {0:"Han", 1:"Jhow", 2:"Jing", 3:"Rick"}

def Training(training_feature, labels, c=1):
    clf = LinearSVC()
    clf.C = c
    clf.fit(training_feature, labels)

    return clf

def Testing(model, testing_feature):
    return model.predict(testing_feature)

def Evalidation(features, labels, k=10):
    training_error = {}
    validation_error = {}

    '''
    for c in [10**x for x in range(-10, 0, 1)]:
        print c
        model.C = c
        tmp_training = []
        tmp_testing  = []
        for i in xrange(k):
            train_idx = np.random.choice(xrange(features.shape[0]), int(0.8*features.shape[0]))
            test_idx  = list(set(xrange(features.shape[0])) - set(train_idx))
            model.fit(features[train_idx], labels[train_idx])
            tmp_training.append(1.0 - model.score(features[train_idx], labels[train_idx]))
            tmp_testing.append(1.0 - model.score(features[test_idx], labels[test_idx]))

        training_error[c] = np.mean(tmp_training)
        validation_error[c] = np.mean(tmp_testing)
    '''
    model = LinearSVC()

    #validation_error[c]=np.mean(cross_validation.cross_val_score(model, features, labels, cv=5))
    kf = cross_validation.KFold(features.shape[0], n_folds=5, shuffle=True)
    for c in [10**x for x in xrange(-10, 0, 1)]:
        tmp_training = []
        tmp_testing  = []
        model.C = c
        for train_idx, test_idx in kf:
            model.fit(features[train_idx], labels[train_idx])

            tmp_training.append(1.0 - model.score(features[train_idx], labels[train_idx]))
            tmp_testing.append(1.0 - model.score(features[test_idx], labels[test_idx]))

        training_error[c] = np.mean(tmp_training)
        validation_error[c] = np.mean(tmp_testing)


    print training_error
    print validation_error

    tmp = open('out.csv', 'w')

    for c in [10**x for x in range(-10, 0, 1)]:
        print c
        tmp.write(','.join(str(x) for x in [c, training_error[c], validation_error[c]]) + '\n')

    tmp.close()
    #print 'Training Error   = ' + str(np.mean(training_error))
    #print 'Validation Error = ' + str(np.mean(validation_error))

