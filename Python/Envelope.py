import numpy as np
def envelope(train_label, train_data, test_data, num_std):
	unique_label = set(train_label)

	s_train = [len(train_data), len(train_data[0])]
	s_test = [len(test_data),len(test_data[0])]
	s_label = len(unique_label)

	mean_train = np.zeros([s_label, s_train[1]])
	std_train =	np.zeros([s_label, s_train[1]])
	for i in range(1,s_label+1):
		now_label_data = []
		label = unique_label.pop()
		# Find the same label's data
		for t in range(len(train_data)):
			if train_label[t] == label:
				now_label_data.append(train_data[t])
		# Compute the mean
		mean_train[i-1] = np.add.reduce(now_label_data) / float(len(now_label_data))

		# Compute the std
		now_label_data = np.transpose(now_label_data)
		std_train[i-1] = [np.std(now_label_data[j]) for j in range(len(now_label_data))]

	envelope_data = np.zeros([s_test[0], 3 * s_label])
	for i in range(s_test[0]):
		for count in range(1,s_label+1):
			num_one = len(np.where(test_data[i] > (mean_train[count-1] + num_std*std_train[count-1]))[0])
			num_mone = len(np.where(test_data[i] < (mean_train[count-1] + num_std*std_train[count-1]))[0])

			envelope_data[i][(count-1)*3] = s_test[1] - num_one - num_mone
			envelope_data[i][(count-1)*3 + 1] = num_one
			envelope_data[i][(count-1)*3 + 2] = num_mone

	return envelope_data
if __name__ == '__main__':
	train_label = [1,1,2,2]
	train_data = [[1,0,1], [1,1,1], [0,0,1], [1,0,1]]
	test_data = [[1,2,1], [1,2,2]]
	num_std = 2
	envelope(train_label, train_data, test_data, num_std)


