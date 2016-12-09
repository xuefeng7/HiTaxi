import time
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
import pickle
from sklearn.model_selection import cross_val_score
## this script trains the three rfrs for three region types
## also, two svrs to compare the outcomes returned from rfr
## then the final model is a combination of three models

# CONSTANT
FEATURE_SIZE = 14
TRAIN_SIZES = [2819503, 158916, 51493]
TRAIN_SETS = ['trainset_2014_type1.txt', 'trainset_2014_type2.txt', 'trainset_2014_type3.txt']

### Training Set Generation
# month,day,hr,weekday,temp,cond,outdoor,home&work,nightlife,
# college&university,food,shop,travel,art&entertain,demand
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

def train_rfr_with(fm, tv, r_type):
	rfr = RandomForestRegressor(n_estimators=120, max_features=FEATURE_SIZE/3, oob_score=True, n_jobs=4)
	print "Training rfr for type " + str(r_type)
	start_time = time.time()
	# rfr.fit(fm, tv)
	# print "Training completed in " + str(time.time() - start_time) + "s"
	# print "rfr oob score: " + str(rfr.oob_score_)
	# print "rfr feature_importances:" + str(rfr.feature_importances_)
	results = cross_val_score(rfr, fm, tv, scoring='neg_mean_squared_error', cv=5, n_jobs=-1)
	print results

def train_svr_with(fm, tv, r_type):
	# standardize fm
	fm = StandardScaler().fit_transform(fm)
	params = {'C':[5, 10, 100]}
	svr = GridSearchCV(SVR(kernel='rbf', cache_size=200), cv=5,
                   param_grid=params, scoring="r2", n_jobs=4)
	print "Training svr(cache_size=200) for type " + str(r_type)
	svr.fit(fm, tv)

	print svr.best_estimator_
	print svr.best_score_

# fms = []
# tvs = []

print "----------- Training for rfr -----------"
for idx in range(3):
	print "generating fm for type " + str(idx + 1)
	fm, tv = read_obser_set(TRAIN_SETS[idx], TRAIN_SIZES[idx])
	# fms.append(fm)
	# tvs.append(tv)
	# no need to standardize for rfr
	train_rfr_with(fm, tv, (idx + 1))

# print "----------- Training for svr -----------"
# for idx in range(1,3):
# 	fm, tv = read_obser_set(TRAIN_SETS[idx], TRAIN_SIZES[idx])
# 	train_svr_with(fm, tv, (idx + 1))
