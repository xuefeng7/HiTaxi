import json

weather = open('weather_processed.txt', 'r')

weather_dict = {}
for line in weather:
	weather_obj = json.loads(line)
	date = weather_obj.keys()[0]
	weather_dict[date] = weather_obj[date]

def re_structure_date(pick_up_time):
	# get date
   	date_comp = (pick_up_time.split('T')[0]).split("-")
   	# get month
   	month = str(int(date_comp[1]))
   	# get day
   	day = str(int(date_comp[2]))
   	date = date_comp[0] + "/" + month + "/" + day

   	time = str(int((pick_up_time.split('T')[1]).split(":")[0]))
   	return {"date":date, "time":time}

trip_dict = []
with open('2014_taxi_trip.txt') as data_file:    
    data = json.load(data_file)
    for trip in data:
   		pick_up_time = re_structure_date(trip['pickup_datetime'])
   		pick_up_loc = {"log":trip["pickup_longitude"], "lat":trip['pickup_latitude']}
   		drop_off_loc =  {"log":trip["dropoff_longitude"], "lat":trip['dropoff_latitude']}
   		passenger = trip["passenger_count"]
   		temp = weather_dict[pick_up_time['date']][pick_up_time['time']]['temp']
   		condition = weather_dict[pick_up_time['date']][pick_up_time['time']]['condition']
   		trip_obj = {
   			"pick_up_time": pick_up_time,
   			"pick_up_loc": pick_up_loc,
   			"drop_off_loc": drop_off_loc,
   			"passenger": passenger,
   			"temp": temp,
   			"condition": condition
   		}
   		trip_dict.append(trip_obj)

print trip_dict
