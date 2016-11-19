import urllib2
import json
from math import cos,asin,sqrt
import datetime
import calendar
import logging
import time
import sys

logging.basicConfig(filename = "debug/debug_"+sys.argv[1]+".log", level = logging.DEBUG)
# load popular cluster dictionary
region_dict = json.loads(open('Clusters.json','r').read())
# load region 
weather_dict = json.loads(open('weather_processed.json','r').read())

# condition category
condition_dict = {
	"normal": ['ScatteredClouds', 'MostlyCloudy', 'PartlyCloudy', 'Clear', 'Overcast', 'Haze', 'Mild', 'Quitecool', 'Chilly', 'Frigid', 'Cold', 'Cool'],
	"heavy_rain": ['Rain', 'HeavyRain'],
	"light_rain": ['LightFreezingRain', 'LightRain'],
	"heavy_snow": ['HeavySnow', 'Snow'],
	"light_snow": ['LightSnow'],
	"fog": ['Fog', 'Mist'],
}

offset = 300 * int(sys.argv[1])
limit = '50000'
link = 'https://data.cityofnewyork.us/resource/gkne-dk5s.json?$limit='+ limit +'&$offset=' + str(offset)
output = open('processed_trip/processed_trips_' + sys.argv[1] + '.txt', 'a+')

##### MAIN FUNCTIONS

# query trips and load them as json objects
def query_trip(link):
	response = urllib2.urlopen(link)
	return json.loads(response.read())

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

	### get the cluster region info of the trip (region)
	# start_time = time.time()
	region_id = get_region_info(trip, pick_up_coord)
	# print "get region_id costs " + str(time.time() - start_time) + " s"
	if region_id == 0:
		# trip far fram all popular regions, ignore it
		return
	### near a popular region, parse it as followings

	## get the time component
	# process pick_up_time in the corresponding format to search weather
	time_arr = (pick_up_time.split("T")[0]).split('-')
	year = time_arr[0]
	month = time_arr[1]
	if month[0] == '0':
		month = month[1]
	date = time_arr[2]
	if date[0] == '0':
		date = date[1]
	hour = (pick_up_time.split("T")[1]).split(':')[0]
	# trim the leading 0 (i.e 07 -> 7)
	if hour[0] == '0':
		hour = hour[1]

	# get weekday
	dateObj = datetime.datetime(int(year),int(month), int(date))
	weekday = dateObj.weekday()

	### get the weather info of the trip (temp, condition)
	weather_info = get_weather_info(pick_up_time, year, month, date, hour)
	temp = weather_info[0]
	condition = get_condition_label(weather_info[1])
	
	# encapsulation
	trip = {
				'pick_up_date': month + '/' + date,
				'pick_up_hour': hour,
				'weekday': (weekday + 1),
				'pick_up_coord': pick_up_coord, 
				'drop_off_coord': drop_off_coord,
				'passenger_count': passenger,
				'temp': temp,
				'condition': condition,
				'region_id': region_id
			}
	return trip

##### AUXULIARY FUNCTIONS
def get_region_info(trip, coord):
	# get trip coordinate bound
	p = 0.017453292519943295
	lower_lat = float(trip['pickup_latitude']) - 1 / 110.574
	upper_lat = float(trip['pickup_latitude']) + 1 / 110.574
	lower_log = float(trip['pickup_longitude']) - 1 / (111.320 * cos(p*float(trip['pickup_latitude'])))
	upper_log = float(trip['pickup_longitude']) + 1 / (111.320 * cos(p*float(trip['pickup_latitude'])))
	
	# search for the nearest region
	# shallow copy
	clusters = []
	for each in region_dict:
		if not (float(str(each['coordinates'][0])) < lower_log or float(str(each['coordinates'][0])) > upper_log or float(str(each['coordinates'][1])) < lower_lat or float(str(each['coordinates'][1])) > upper_lat):
			#print each['coordinates'][0]
			clusters.append(each)

	min = 1138
	index = 0
	for each in clusters:
		dist = distance(float(str(each['coordinates'][1])), float(str(each['coordinates'][0])), float(str(coord['lat'])), float(str(coord['log'])))	
		if min > dist:
			min = dist
			index = each['index']
	return index

def get_weather_info(pick_up_time, year, month, date, hour):
	
	# the key for searching weather in weather dict
	year_search_key = year + '/' + month + '/' + date
	

	temp = weather_dict[year_search_key][hour]['temp']
	condition = weather_dict[year_search_key][hour]['condition']
	return [temp, condition]

# convert raw condition to condition label
def get_condition_label(condition):
	for key in condition_dict.keys():
		if condition in condition_dict[key]:
			return key

# given two coordinate, comput their distance
def distance(lat1, lon1, lat2, lon2):
	p = 0.017453292519943295
	a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
	return (12742 * asin(sqrt(a)))


##### MAIN QUERY LOOPS


offset_upper_bound = 300 * (int(sys.argv[1]) + 1) - 1
cp_processed_trip_count = 0 # current page processed count
skip = 0

while offset < offset_upper_bound :
	
	# start_time = time.time()
	try:
		trips = query_trip(link)
		# print "file " + sys.argv[1] +": " + "query costs " + str(time.time() - start_time) + " s"
		#start_time = time.time()
		for trip in trips:
			cp_processed_trip_count += 1
			if cp_processed_trip_count > skip:
				logging.debug("processing trip no." + str(cp_processed_trip_count) + " at page." + str(offset))
				#print trip
				#print parse_trip(trip)
				try:
					if parse_trip(trip) is not None:
						# dump to json output
						trip_obj = parse_trip(trip)
						output.write(json.dumps(trip_obj) + '\n')
				except Exception as e:
					# write error message and trip index to error file
					errMsg = "processing trip no." + str(cp_processed_trip_count) + " at page." + str(offset) + ' failed: ' + str(e)
					logging.debug(errMsg)
					pass
		# print "file " + sys.argv[1] +": " + "process costs " + str(time.time() - start_time) + "s"
		offset += 1
		cp_processed_trip_count = 0
	except Exception as e:
		# write error message and trip index to error file
		errMsg = "file " + sys.argv[1] +": " + "Query Page no." + str(offset) + ' failed: ' + str(e)
		logging.debug(errMsg)
		pass


logging.debug("file " + sys.argv[1] + ": " + "trip processing is completed")