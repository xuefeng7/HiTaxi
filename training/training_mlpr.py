# MLP regression
import time
import numpy as np
import sklearn.neural_network.MLPRegressor as MLPR

# CONSTANT
FEATURE_SIZE = 14
TRAIN_SIZE = 3029912
TEST_SIZE = 1477769

weather_code = {
	'normal': 0,
	'heavy_rain': 1,
	'light_rain': 2,
	'heavy_snow': 3,
	'light_snow': 4,
	'fog': 5
}

### Training Set Generation
def read_obser_set(set_name, SIZE):
	feature_matrix = np.empty(shape=(SIZE, FEATURE_SIZE), dtype="S15")
	truth_vector = np.zeros(shape=(SIZE, ))
	# read in observation set
	with open(set_name) as tf:
		obser_count = 0
		for observation in tf:
			observation = observation.split(",")
			observation = [item.strip(' ') for item in observation]
			# region = observation[0]
			# use numeric representation of month and date
			# month
			month = int(observation[1].split("/")[0])
			# date
			date = int(observation[1].split("/")[1])
			# hr
			hr = int(observation[2])
			# weekday
			weekday = int(observation[3])
			# use digit to represent weather condition
			cond_code = weather_code[observation[5].split('(')[0]]
			# temp
			temp = float(observation[4])
			# the last element is the ground truth of the demanding count
			truth = int(observation[6].replace("\\","").replace("n",""))
			# facilities
			factility = []
			for idx in range(7,15):
				factility.append(int(observation[idx]))
			# input features
			feature_matrix[obser_count] = [month, date, hr, weekday, temp, cond_code] + factility
			# input truth
			truth_vector[obser_count] = truth
			obser_count += 1
	return [feature_matrix, truth_vector]

print "generating training matrix ..."
train_feature_matrix, train_truth_vector = read_obser_set('trainset_2014_with_facility.txt', TRAIN_SIZE)
### Testing Set Generation
print "generating testing matrix ..."
test_feature_matrix, test_truth_vector = read_obser_set('trainset_2015_with_facility.txt', TEST_SIZE)

### Model building
# parameters = {'C':[1, 10]}
# svr = SVR(kernel='rbf')
# clf = GridSearchCV(svr, parameters,  n_jobs=6, cv=3)
# # standardize the training feature matrix
# feature_matrix = StandardScaler().fit_transform(feature_matrix)
# clf.fit(train_feature_matrix, train_truth_vector)
layer_sizes = [100, 200, 300]
for layer_size in layer_size:
	print "Training for mlp with " + str(layer_size) + " layers"
	start_time = time.time()
	mlpr = MLPR(hidden_layer_sizes=(layer_size, ))
	mlpr.fit(train_feature_matrix, train_truth_vector)
	print "Training completed in " + str(time.time() - start_time) + "s"
	print "the loss: " + str(mlpr.loss_)
	start_time = time.time()
	score = mlpr.score(test_feature_matrix, test_truth_vector)
	print "Testing completed in " + str(time.time() - start_time) + "s"
	print "-----------------------------------------"
