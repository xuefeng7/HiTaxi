import urllib2
import json
from math import cos,asin,sqrt
import datetime
import calendar


# load popular cluster dictionary
weather_dict = json.loads(open('weather_processed.json','r').read())
# region dictionary
region_dict = {}

offset = 0
limit = '100'
link = 'https://data.cityofnewyork.us/resource/gkne-dk5s.json?$limit='+ limit +'&$offset=' + str(offset)
# output = open('trips_processed.json', 'a+')

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
	region_id = get_region_info(trip, pick_up_coord)
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

	# get weekday
	dateObj = datetime.datetime(int(year),int(month), int(date))
	weekday = dateObj.weekday()

	### get the weather info of the trip (temp, condition)
	weather_info = get_weather_info(pick_up_time, year, month, date)
	temp = weather_info[0]
	condition = weather_info[1]
	
	# encapsulation
	trip = {
				'pick_up_time': pick_up_time,
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
	lowerlat = float(trip['pickup_latitude']) - 1 / 110.574
	upperlat = float(trip['pickup_latitude']) + 1 / 110.574
	lowerlog = float(trip['pickup_longitude']) - 1 / (111.320 * cos(p*float(trip['pickup_latitude'])))
	upperlog = float(trip['pickup_longitude']) + 1 / (111.320 * cos(p*float(trip['pickup_latitude'])))
	
	# search for the nearest region
	with open('Clusters.json','r') as input:
		clusters = json.load(input)
		for each in clusters:
			if float(str(each['coordinates'][0])) < lowerlog or float(str(each['coordinates'][0])) > upperlog or float(str(each['coordinates'][1])) < lowerlat or float(str(each['coordinates'][1])) > upperlat:
				#print each['coordinates'][0]
				clusters.remove(each)

	min = 1138
	index = 0
	for each in clusters:
		dist = distance(float(str(each['coordinates'][1])), float(str(each['coordinates'][0])), float(str(coord['lat'])), float(str(coord['log'])))	
		if min > dist:
			min = dist
			index = each['index']
	return index

def get_weather_info(pick_up_time, year, month, date):
	# the key for searching weather in weather dict
	year_search_key = year + '/' + month + '/' + date
	hour_search_point = (pick_up_time.split("T")[1]).split(':')[0]
	
	# trim the leading 0 (i.e 07 -> 7)
	if hour_search_point[0] == '0':
		hour_search_point = hour_search_point[1]

	temp = weather_dict[year_search_key][hour_search_point]['temp']
	condition = weather_dict[year_search_key][hour_search_point]['condition']
	return [temp, condition]


# given two coordinate, comput their distance
def distance(lat1, lon1, lat2, lon2):
	p = 0.017453292519943295
	a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
	return (12742 * asin(sqrt(a)))


for trip in query_trip(link):
	#print trip
	print parse_trip(trip)
