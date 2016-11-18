import urllib2
import json
<<<<<<< HEAD
from math import cos,asin,sqrt

=======
import datetime
import calendar
>>>>>>> origin/master

# load popular cluster dictionary
weather_dict = json.loads(open('weather_processed.json','r').read())
# region dictionary
region_dict = {}

offset = 0
limit = '1'
link = 'https://data.cityofnewyork.us/resource/gkne-dk5s.json?$limit='+ limit +'&$offset=' + str(offset)
# output = open('trips_processed.json', 'a+')

##### MAIN FUNCTIONS
# query trips and load them as json objects
def query_trip(link):
	response = urllib2.urlopen(link)
	return json.loads(response.read())

def distance(lat1, lon1, lat2, lon2):
	p = 0.017453292519943295
	a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
	return (12742 * asin(sqrt(a)))

def get_center(clusters):
	min = 1138
	index = 0
	for each in clusters:
		if min > distance(clusters['radius']):
			min = clusters['radius']
			index = clusters['index']
	return index

# take a trip and 
# 1. get pick_up/drop_off geo-locations
# 	 get time of trip, passenger #, 
# 	 and weather data
# 2. according to the pick_up geo-location, cluster the trip to region
# 3. write json object into file
def parse_trip(trip):

	### get basic info of trip (time, coord, passenger)
	pick_up_time = trip['pickup_datetime']
	pick_up_coord = {'lat':trip['pickup_latitude'], 'log': trip['pickup_longitude']}
	drop_off_coord = {'lat':trip['dropoff_latitude'], 'log': trip['dropoff_longitude']}
	passenger = trip['passenger_count']
	lowerlat = float(trip['pickup_latitude']) - 1 / 110.574
	upperlat = float(trip['pickup_latitude']) + 1 / 110.574
	lowerlog = float(trip['pickup_longitude']) - 1 / (111.320 * cos(float(trip['pickup_latitude'])))
	upperlog = float(trip['pickup_longitude']) + 1 / (111.320 * cos(float(trip['pickup_latitude'])))

	## get the time component
	# process pick_up_time in the corresponding format to search weather
	time_arr = (pick_up_time.split("T")[0]).split('-')
	year = time_arr[0]
	month = time_arr[1]
	date = time_arr[2]

	# get weekday
	dateObj = datetime.datetime(int(year),int(month), int(date))
	weekday = dateObj.weekday()

	### get the weather info of the trip (temp, condition)
	weather_info = get_weather_info(year, month, date)
	temp = weather_info[0]
	condition = weather_info[1]
	
	### get the cluster region info of the trip (region)

	with open('Clusters.json','r') as input:
		clusters = json.load(input)
	if get_center(clusters) == 0:
		return
	
	# encapsulation
	trip = {
				'pick_up_time': pick_up_time,
				'weekday': weekday,
				'pick_up_coord': pick_up_coord, 
				'drop_off_coord': drop_off_coord,
				'passenger_count': passenger,
				'temp': temp,
				'condition': condition,
				'region_id': get_center(clusters)
			}
	return trip

##### AUXULIARY FUNCTIONS
def get_weather_info(year, month, date):
	# the key for searching weather in weather dict
	year_search_key = year + '/' + month + '/' + date
	hour_search_point = (pick_up_time.split("T")[1]).split(':')[0]
	
	# trim the leading 0 (i.e 07 -> 7)
	if hour_search_point[0] == '0':
		hour_search_point = hour_search_point[1]

	temp = weather_dict[year_search_key][hour_search_point]['temp']
	condition = weather_dict[year_search_key][hour_search_point]['condition']
	return [temp, condition]

# def get_region_info(coord):

# def get_distance(log_1, lat_1, log_2, lat_2):


for trip in query_trip(link):
	print parse_trip(trip)



