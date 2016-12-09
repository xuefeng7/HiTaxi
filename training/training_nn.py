## using keras to build a neural netwrok model
import os
# switch backend
os.environ["KERAS_BACKEND"] = "theano"

import numpy as np
import pandas
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import pickle
import time
# CONSTANT
FEATURE_SIZE = 14
TRAIN_SIZE = 3029912
TEST_SIZE = 1477769

EPOCH = 100
BATCH_SIZE =20

WEATHER_CODE = {
	'normal': 0,
	'heavy_rain': 1,
	'light_rain': 2,
	'heavy_snow': 3,
	'light_snow': 4,
	'fog': 5
}

### Training Set Generation
def read_obser_set(set_name, SIZE):
	feature_matrix = np.empty(shape=(SIZE, FEATURE_SIZE))
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
			cond_code = WEATHER_CODE[observation[5].split('(')[0]]
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

print "reading data..."
train_feature_matrix, train_truth_vector = read_obser_set('trainset_2014_with_facility.txt', TRAIN_SIZE)

# creating model
def deep_network_model():
	model = Sequential()
	model.add(Dense(FEATURE_SIZE/2, input_dim=FEATURE_SIZE, init='normal', activation='relu'))
	model.add(Dense(FEATURE_SIZE/2, init='normal', activation='relu'))
	model.add(Dense(FEATURE_SIZE/2, init='normal', activation='relu'))
	model.add(Dense(FEATURE_SIZE/2, init='normal', activation='relu'))
	model.add(Dense(FEATURE_SIZE/2, init='normal', activation='relu'))
	model.add(Dense(1, init='normal'))
	# Compile model
	model.compile(loss='mean_squared_error', optimizer='adam')
	return model

# creating model
def wider_network_model():
	model = Sequential()
	model.add(Dense(FEATURE_SIZE*4, input_dim=FEATURE_SIZE, init='normal', activation='relu'))
	model.add(Dense(FEATURE_SIZE*2, init='normal', activation='relu'))
	model.add(Dense(FEATURE_SIZE*2, init='normal', activation='relu'))
	model.add(Dense(FEATURE_SIZE*2, init='normal', activation='relu'))
	model.add(Dense(FEATURE_SIZE*2, init='normal', activation='relu'))
	model.add(Dense(1, init='normal'))
	# Compile model
	model.compile(loss='mean_squared_error', optimizer='adam')
	return model

# k-fold cv for performance evaluation
def evaluate(estimator, x, y, k):
	kfold = KFold(n_splits=k, random_state=seed)
	results = cross_val_score(estimator, x, y, cv=kfold)
	print("Results: %.2f (%.2f) MSE" % (results.mean(), results.std()))

# print "nn: epoch=" + str(EPOCH) + ", batch_size=" + str(BATCH_SIZE) + ", hidden_layer=4"
# # fix random seed for reproducibility
# print "training estimator..."
seed = 7
# estimators = []
# estimators.append(('standardize', StandardScaler()))
# # we have 3029912 training examples, and the batch size is 500, then it will take 2 iterations to complete 1 epoch.
# estimators.append(('mlp', KerasRegressor(build_fn=deep_network_model, nb_epoch=EPOCH, batch_size=BATCH_SIZE, verbose=0)))
# pipeline = Pipeline(estimators)
# # evaluate model with standardized dataset
# # larger batch size requires larger memory space, but will improve the model
# # estimator = KerasRegressor(build_fn=network_model, nb_epoch=100, batch_size=5, verbose=0)
# print "evaluating estimator..."
# start_time = time.time()
# evaluate(pipeline, train_feature_matrix, train_truth_vector, 5)
# print "evaluting costs " + str(time.time() - start_time) + "s"


print "nn: epoch=" + str(EPOCH) + ", batch_size=" + str(BATCH_SIZE) + ", wider_hiddeb_layer=4"
# fix random seed for reproducibility
print "training estimator..."
estimators = []
estimators.append(('standardize', StandardScaler()))
# we have 3029912 training examples, and the batch size is 500, then it will take 2 iterations to complete 1 epoch.
estimators.append(('mlp', KerasRegressor(build_fn=wider_network_model, nb_epoch=EPOCH, batch_size=BATCH_SIZE, verbose=0)))
pipeline = Pipeline(estimators)
# evaluate model with standardized dataset
# larger batch size requires larger memory space, but will improve the model
# estimator = KerasRegressor(build_fn=network_model, nb_epoch=100, batch_size=5, verbose=0)
print "evaluating estimator..."
start_time = time.time()
evaluate(pipeline, train_feature_matrix, train_truth_vector, 5)
print "evaluting costs " + str(time.time() - start_time) + "s"
