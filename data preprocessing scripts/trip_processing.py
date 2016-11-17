import urllib2
import json

# load popular cluster dictionary
weather_dict = json.loads(open('weather_processed.json','r').read())
# region dictionary
region_dict = {}

offset = 0
link = 'https://data.cityofnewyork.us/resource/gkne-dk5s.json?$limit=2&' + '$offset=' + str(offset)
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

	### get basic info of trip
	pick_up_time = trip['pickup_datetime']
	pick_up_coord = {'lat':trip['pickup_latitude'], 'log': trip['pickup_longitude']}
	drop_off_coord = {'lat':trip['dropoff_latitude'], 'log': trip['dropoff_longitude']}
	passenger = trip['passenger_count']

	### get the weather info of the trip
	# process pick_up_time in the corresponding format to search weather
	time_arr = (pick_up_time.split("T")[0]).split('-')
	year = time_arr[0]
	month = time_arr[1]
	date = time_arr[2]
	# the key for searching weather in weather dict
	year_search_key = year + '/' + month + '/' + date
	hour_search_point = (pick_up_time.split("T")[1]).split(':')[0]
	if hour_search_point[0] == '0': #trim the leading 0 (i.e 07 -> 7)
		hour_search_point = hour_search_point[1]
	print hour_search_point
	temp = weather_dict[year_search_key][hour_search_point]['temp']
	condition = weather_dict[year_search_key][hour_search_point]['condition']
	
	### get the cluster region info of the trip

	# encapsulation
	trip = {
				'pick_up_time': pick_up_time, 
				'pick_up_coord': pick_up_coord, 
				'drop_off_coord': drop_off_coord,
				'passenger_count': passenger,
				'temp': temp,
				'condition': condition,
				'region_id': ""
			}
	return trip

##### AUXULIARY FUNCTIONS
# def get_distance(log_1, lat_1, log_2, lat_2):


for trip in query_trip(link):
	print parse_trip(trip)

