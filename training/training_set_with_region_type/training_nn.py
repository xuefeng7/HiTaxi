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
from sklearn.externals import joblib
import time

# CONSTANT
FEATURE_SIZE = 14
TRAIN_SIZES = [2819503, 158916, 51493]
TRAIN_SETS = ['trainset_2014_type1.txt', 'trainset_2014_type2.txt', 'trainset_2014_type3.txt']

EPOCH = 1000
BATCH_SIZE =20

WEATHER_CODE = {
	'normal': 0,
	'heavy_rain': 1,
	'light_rain': 2,
	'heavy_snow': 3,
	'light_snow': 4,
	'fog': 5
}

def read_obser_set(set_name, SIZE):
	feature_matrix = np.empty(shape=(SIZE, FEATURE_SIZE))
	truth_vector = np.zeros(shape=(SIZE, ))
	# read in observation set
	with open(set_name) as tf:
		obser_count = 0
		for observation in tf:
			observation = observation.split(",")
			observation = [float(feature) for feature in observation]
			# input truth
			truth_vector[obser_count] = observation.pop()
			feature_matrix[obser_count] = observation
			obser_count += 1
	return [feature_matrix, truth_vector]

print "reading data..."

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
	seed = 7
	kfold = KFold(n_splits=k, random_state=seed)
	results = cross_val_score(estimator, x, y, scoring='r2', cv=kfold, n_jobs=-1)
	print results
	

def train_with_nn(fm, tv, r_type):
	print "generating fm for type " + str(r_type + 1)
	print "nn: epoch=" + str(EPOCH) + ", batch_size=" + str(BATCH_SIZE) + ", wider_hiddeb_layer=4"
	fm, tv = read_obser_set(TRAIN_SETS[idx], TRAIN_SIZES[idx])
	# standardize fm
	fm = StandardScaler().fit_transform(fm)
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
	evaluate(pipeline, fm, tv, 5)
	print "evaluting costs " + str(time.time() - start_time) + "s"
	print "saving estimator..."
	joblib.dump(estimators, 'model_type_' + str(r_type + 1) +'.pkl') 


for idx in range(1, 3):
	fm, tv = read_obser_set(TRAIN_SETS[idx], TRAIN_SIZES[idx])
	train_with_nn(fm, tv, idx)




