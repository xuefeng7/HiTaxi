import time
import numpy as np
from sklearn.ensemble import RandomForestRegressor
# from sklearn.model_selection import GridSearchCV
### read through training observation from files
### create feature matrix

# CONSTANT
FEATURE_SIZE = 6
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
			# use numeric representation of month and date
			observation[1] = observation[1].replace("/","")
			# use digit to represent weather condition
			observation[5] = weather_code[observation[5].split('(')[0]]
			# the last element is the ground truth of the demanding count
			truth = int(observation.pop())
			# input features
			feature_matrix[obser_count] = observation
			# input truth
			truth_vector[obser_count] = truth
			obser_count += 1
	return [feature_matrix, truth_vector]

print "generating training matrix ..."
train_feature_matrix, train_truth_vector = read_obser_set('trainset_2014.txt', TRAIN_SIZE)
### Testing Set Generation
print "generating testing matrix ..."
test_feature_matrix, test_truth_vector = read_obser_set('trainset_2015_.txt', TEST_SIZE)

### Model Building and Learning
# basic model = random forest regressor
# Hyper-Params:
# 1. n_estimator: max number of trees in the forest, more trees means better accuracy
# in the trade of training time
# 2. oob_score: out-of-bag correctness, the higher the score, the better the accuracy
# 3. n_jobs: concurrency.
# TUNING TODO: max_features
# 
# params_grid = {"max_features":[1, 2, 3], "bootstrap": [True, False], "n_estimators":[100, 200, 300]}
#GridSearchCV(RandomForestRegressor(oob_score=True, n_jobs=6), cv=10, param_grid=params_grid)
rfr = RandomForestRegressor(n_estimators=100, max_features=FEATURE_SIZE, oob_score=True, n_jobs=6)
print "Training..."
start_time = time.time()
rfr.fit(train_feature_matrix, train_truth_vector)
print "Training completed in " + str(time.time() - start_time) + "s"
print "rfr oob score: " + str(rfr.oob_score_)
print "rfr feature_importances:" + str(rfr.feature_importances_)

print "Testing..."
start_time = time.time()
score = rfr.score(test_feature_matrix, test_truth_vector)

print "Testing completed in " + str(time.time() - start_time) + "s"
print "prediction score: " + str(score)
