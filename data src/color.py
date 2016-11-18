import json

weathers = json.loads(open('weather_processed.json').read())
conditions = {}
count = 0
for key, value in weathers.items():
	count += 1
	for item in value.items():
		condition = item[1]['condition']
		if condition in conditions.keys():
			conditions[condition] += 1
		else:
			conditions[condition] = 1

print conditions
# output = open('weather_processed.json', 'w+')
# weathers = {}
# with open('weather_processed.txt') as f:
#     for line in f:
#       jobj = json.loads(line)
#       key = jobj.keys()[0]
#       weathers[key] =  jobj[key]

# json.dump(weathers, output)
        


