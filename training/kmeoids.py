# from sklearn.cluster import KMeans
# import numpy as np
# import matplotlib as plt
from pylab import *
import collections
import copy
import pdb
import numpy as np
from scipy.spatial.distance import cdist
import random
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import pyclust

# CONSTANT
FEATURE_SIZE = 14
SIZE = 3029912

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
			month = observation[1].split("/")[0]
			# date
			date = observation[1].split("/")[1]
			# hr
			hr = observation[2]
			# weekday
			weekday = observation[3]
			# use digit to represent weather condition
			cond_code = str(weather_code[observation[5].split('(')[0]])
			# temp
			temp = observation[4]
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
train_feature_matrix, train_truth_vector = read_obser_set('trainset_2014_with_facility.txt', SIZE)
print "Standardizing..."
train_feature_matrix = StandardScaler().fit_transform(train_feature_matrix)
print "clustering..."
kmd = pyclust.KMedoids(n_clusters=300000, n_trials=50)
kmd.fit(train_feature_matrix)
# ## K-meoids
# # kmeans = KMeans(n_clusters=30000, init='k-means++', n_jobs=4, algorithm='auto').fit(train_feature_matrix)
# medoids, clusters = kMedoids(np.transpose(train_feature_matrix), 30000)
print "printing..."
centers = open('training_subsample.txt','a+')
for idx in medoids:
	centers.write(str(train_feature_matrix[idx]).replace("]","").replace("[","").replace('\'',"").replace(" ",",") + "," + str(train_truth_vector[0]) + "\n")

centers.close()
	


