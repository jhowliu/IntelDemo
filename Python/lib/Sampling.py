import numpy as np

def OverSampling(data):
    unq, unq_idx, unq_cnt = np.unique(data[:, -1], return_inverse=True, return_counts=True)
    cnt = np.max(unq_cnt)
    out = np.empty((cnt*len(unq), ) + data.shape[1:], data.dtype)
    for i in xrange(len(unq)):
        idx = np.random.choice(np.where(unq_idx==i)[0], cnt)
        out[i*cnt:(i+1)*cnt] = data[idx]

    return out

if __name__ == '__main__':
    data = np.array([[1,2,2,1],
                     [1,2,3,1],
                     [1,2,4,1],
                     [6,7,8,0],
                     [7,8,9,0]])

    print OverSampleing(data)
