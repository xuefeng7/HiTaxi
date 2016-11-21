### raw observation:

# {"pick_up_date": "5/5", 
# "passenger_count": "1", "weekday": 1, "pick_up_coord": {"lat": "40.762587000000003", "log": "-73.967387000000002"}, 
# "region_id": 194, "drop_off_coord": {"lat": "40.840311999999997", "log": "-73.940185"}, 
# "condition": "normal", "pick_up_hour": "21", "temp": "62.1"}

# turn into the following training observation:
# [region_id, date, weekday, hr, temp, weather_condition | passenger count]
# 500 x 365 x 24 = 4.38 million training observations

import json

def parse_raw_trip_for_file(file_name):
	# count total passenger counts for each time slot
	# initialize dictionary by region id
	id_ls = [id for id in range(1, 501)]
	merge_dict = {key:{} for key in id_ls}

	with open(file_name) as f:
	    for line in f:
	       raw_observation = json.loads(line)
	       ## keys
	       region_id = int(str(raw_observation['region_id']))
	       date = str(raw_observation['pick_up_date'])
	       weekday = str(raw_observation['weekday'])
	       hr = str(raw_observation['pick_up_hour'])
	       ## core value
	       temp = raw_observation['temp']
	       cond = raw_observation['condition']
	       count = int(raw_observation['passenger_count'])

	       if date in merge_dict[region_id]:
	       		# already encountered before
	       		if hr in merge_dict[region_id][date]:
	       			# get the old count
	       			val = merge_dict[region_id][date][hr]['count'] + count
	       			merge_dict[region_id][date][hr]['count'] = val

	       		else:
	       			merge_dict[region_id][date][hr] = {'temp': temp, 'cond': cond, 'count': count}
	       else:
	       		# create new one
	       		merge_dict[region_id][date]= {}
	       		merge_dict[region_id][date][hr] = {'temp': temp, 'cond': cond, 'count': count}
	       		merge_dict[region_id][date]['weekday'] = weekday

	return merge_dict


def dumps_dict_to_output(merge_dict, output):
	for region_id in merge_dict.keys():
		for date in merge_dict[region_id].keys():
			for hr in merge_dict[region_id][date].keys():
				# ignore weekday
				if hr is 'weekday':
					continue
				# get values
				weekday = merge_dict[region_id][date]['weekday']
				temp = merge_dict[region_id][date][hr]['temp']
				cond = merge_dict[region_id][date][hr]['cond']
				count =  merge_dict[region_id][date][hr]['count']
				# construct obser str
				observation = str(region_id) + ',' + date + ',' + weekday + "," + hr + ',' + temp + ',' + cond + ',' + str(count) + "\n"
				# dumps
				output.write(observation)

output = open('traning_set.txt', 'a+')

# for file in files:
print "creating merge dict ... "
merge_dict = parse_raw_trip_for_file('processed_trips_0.txt')
print "dumping to output ... "
dumps_dict_to_output(merge_dict, output)

