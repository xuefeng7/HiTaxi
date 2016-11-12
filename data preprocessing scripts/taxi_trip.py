import json

trip = json.load(open('2014_taxi_trip.txt').read())
weather = open('weather_processed.txt', 'r')

weather_dict = {}
for line in weather:
	weather_obj = json.dumps(line)
	date = weather_obj.keys()[0]
	weather_dict[date] = weather_obj[date]





