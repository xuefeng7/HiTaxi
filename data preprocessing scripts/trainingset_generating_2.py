import os, json

out = {}
for i in range(10):
	with open("processed_trips_"+str(i)+".txt") as f:
		print 'processing file ' + str(i)
		for line in f:
			raw_observation = json.loads(line)
			## keys
			region_id = str(raw_observation['region_id'])
			date = str(raw_observation['pick_up_date'])
			hr = str(raw_observation['pick_up_hour'])
			## core value
			count = int(raw_observation['passenger_count'])
			cond = region_id + ',' + date + ','+ hr
			if cond in out:
				out[cond] += count
			else:
				out[cond] = count
with open('trainingset.txt','w+') as g:
	for key in out:
		trainingset.write(key + ',' + str(count) + '\n')


