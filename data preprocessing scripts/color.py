import json

output = open('weather_processed.json', 'w')
weathers = {}
with open('weather_processed.txt') as f:
    for line in f:
      jobj = json.loads(line)
      key = jobj.keys()[0]
      weathers[key] =  jobj[key]

json.dump(weathers, output)
        


