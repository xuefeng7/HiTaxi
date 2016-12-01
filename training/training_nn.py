## using keras to build a neural netwrok model
import numpy as np
import pandas
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import time
# CONSTANT
FEATURE_SIZE = 6
TRAIN_SIZE = 3029912
TEST_SIZE = 1477769

WEATHER_CODE = {
	'normal': 0,
	'heavy_rain': 1,
	'light_rain': 2,
	'heavy_snow': 3,
	'light_snow': 4,
	'fog': 5
}

# load dataset
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
			observation[5] = WEATHER_CODE[observation[5].split('(')[0]]
			# the last element is the ground truth of the demanding count
			truth = int(observation.pop())
			# input features
			feature_matrix[obser_count] = observation
			# input truth
			truth_vector[obser_count] = truth
			obser_count += 1
	return [feature_matrix, truth_vector]

print "reading data..."
train_feature_matrix, train_truth_vector = read_obser_set('trainset_2014.txt', TRAIN_SIZE)

# creating model
def network_model():
	model = Sequential()
	model.add(Dense(FEATURE_SIZE, input_dim=FEATURE_SIZE, init='normal', activation='relu'))
	model.add(Dense(FEATURE_SIZE/2, init='normal', activation='relu'))
	model.add(Dense(1, init='normal'))
	# Compile model
	model.compile(loss='mean_squared_error', optimizer='adam')
	return model

# k-fold cv for performance evaluation
def evaluate(estimator, x, y, k):
	kfold = KFold(n_splits=k, random_state=seed)
	results = cross_val_score(estimator, x, y, cv=kfold)
	print("Results: %.2f (%.2f) MSE" % (results.mean(), results.std()))


# fix random seed for reproducibility
print "training estimator..."
seed = 7
estimators = []
estimators.append(('standardize', StandardScaler()))
estimators.append(('mlp', KerasRegressor(build_fn=baseline_model, nb_epoch=100, batch_size=10, verbose=0)))
pipeline = Pipeline(estimators)
# evaluate model with standardized dataset
# larger batch size requires larger memory space, but will improve the model
# estimator = KerasRegressor(build_fn=network_model, nb_epoch=100, batch_size=5, verbose=0)
print "evaluating estimator..."
start_time = time.time()
evaluate(pipeline, train_feature_matrix, train_truth_vector, 5)
print "evaluting costs " + str(time.time() - start_time) + "s"