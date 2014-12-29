import numpy as np

def envelope(train_label, train_data, test_data, num_std):
    unique_label = set(train_label)
    s_train = [len(train_data), np.max([np.max(map(lambda x: len(x), train_data)),len(test_data[0])])]
    s_test  = [len(test_data),len(test_data[0])]
    s_label = len(unique_label)

    mean_train = np.zeros([s_label, s_train[1]])
    std_train = np.zeros([s_label, s_train[1]])

    for i in range(s_label):
        now_label_data = []
        label = unique_label.pop()
        # Find the same label's data
        for t in range(len(train_data)):
                if train_label[t] == label:
                        now_label_data.append(train_data[t])
        # Compute the mean
        mean_train[i][:len(now_label_data[0])] = np.mean(now_label_data, axis=0)

        # Compute the std
        std_train[i][:len(now_label_data[0])]  = np.std(now_label_data, axis=0)

    envelope_data = np.zeros([s_test[0], 3 * s_label])

    for count in range(0, s_label):
        num_one   = np.sum(test_data > mean_train[count][:len(test_data[0])] + num_std * std_train[count][:len(test_data[0])], 1)
        num_minus = np.sum(test_data < mean_train[count][:len(test_data[0])] - num_std * std_train[count][:len(test_data[0])], 1)
        envelope_data[:, (count)*3] = s_test[1] - num_one - num_minus
        envelope_data[:, (count)*3 + 1] = num_one
        envelope_data[:, (count)*3 + 2] = num_minus

    return envelope_data

if __name__ == '__main__':
    train_label = [1,1,2,2]
    train_data = [[1,0,1], [1,1,1], [0,0,1,1], [1,0,1,1]]
    test_data = [[1,1,1], [1,2,2]]
    num_std = 1
    print envelope(train_label, train_data, test_data, num_std)


