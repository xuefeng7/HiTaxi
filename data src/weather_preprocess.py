## weather data preprocessing
import json
import collections

# raw = open('weather.txt', 'r')
processed = open('weather_processed.txt', 'r')
# count = 0
# for line in raw:
# 	new_dict = {}
# 	obj = json.loads(line)
# 	date = obj.keys()[0]
# 	new_dict[date] = {}
# 	keys = obj[date].keys()
# 	for key in keys:
# 		if "PM" in key:
# 			if "12:" in key:
# 				new_key = int(key.split(":")[0])
# 			else:
# 				new_key = int(key.split(":")[0]) + 12
# 		elif "12:" in key:
# 			new_key = 0
# 		else:
# 			new_key = int(key.split(":")[0])
# 		new_dict[date][new_key] = obj[date][key]
# 		new_dict[date] = collections.OrderedDict(sorted(new_dict[date].items()))
# 	json_str = json.dumps(new_dict)
# 	processed.write(json_str + "\n")
count = 0
line_c = 0
for line in processed:
	line_c += 1
	obj = json.loads(line)
	date = obj.keys()[0]
	keys = obj[date].keys()
	if len(keys) != 24:
		print line_c
		print str(len(keys)) + "---"
	# all_known = True
	# for key in keys:
	# 	if obj[date][key]["condition"] == "Unknown":
	# 		all_known = False
	# if not all_known:
	# 	print "line. " + str(line_c)
	# 	count += 1

print count



