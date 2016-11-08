import urllib2
import json
import re
import time
from datetime import date, datetime, timedelta

# construct the query url
# https://www.wunderground.com/history/airport/KNYC/2014/10/7/DailyHistory.html?
# req_city=New+York&req_state=NY&req_statename=New+York&reqdb.zip=10001&reqdb.magic=11&reqdb.wmo=99999

# produce date stream
def perdelta(start, end, delta):
    curr = start
    while curr < end:
        yield curr
        curr += delta

# build the query url
def build_query_url(date):
	url = "https://www.wunderground.com/history/airport/KNYC/" + date + "/DailyHistory.html?req_city=New+York&req_state=NY" + "&req_statename=New+York&reqdb.zip=10001&reqdb.magic=11&reqdb.wmo=99999"
	return url

# send request to get full page src
def send(url):
	response = urllib2.urlopen(url)
	return response.read() 

# parse the html and 
# get all useful info into weather dict
def parse_html(html, date):
	weather_dict = {}
	weather_dict[date] = {}
	# hourly dictionary
	html_src = html.split("\n")
	inrow = False
	column = 0
	data = ["", "", ""]
	head_count = -1 # how many column in the table, c_1 -> temp, c_last -> condition
	encounter_hourly_data = False
	for line in html_src:
		line = line.strip('\t\n\r').replace(" ", "")
		# get the table
		# after match each hour
		# the information comes in the following order:
		if "HourlyWeatherHistory" in line:
			encounter_hourly_data = True
		if encounter_hourly_data and "<th>" in line:
			head_count += 1
		if bool(re.match(r'<td>\d{1,}:\d{1,}(AM|PM)</td>', line)):
			hour = re.search(r'\d{1,}:\d{1,}(AM|PM)', line).group(0)
			weather_dict[date][hour] = {}
			inrow = True
		if inrow:
			if column == 1:
				# temp
				data[0] += line
			# if column == 6:
			# 	# visibility
			# 	data[1] += line
			if column == head_count:
				# condition 
				data[2] += line
			if column == (head_count + 1):
				inrow = False
				column = 0
				# match temp
				if bool(re.match(r'<td>-</td>', data[0])):
					weather_dict[date][hour]["temp"] = "-"
				else:
					weather_dict[date][hour]["temp"] = re.search(r'\d{1,}\.\d{1,}', data[0]).group(0)
				# match visibility
				# weather_dict[date][hour]["visibility"] = re.search(r'\d{1,}\.\d{1,}', data[1]).group(0)
				# match condition
				weather_dict[date][hour]["condition"] = re.search(r'>\w{1,}<', data[2]).group(0).replace(">", "").replace("<", "")
				data = ["", "", ""]
			if "</td>" in line:
				column += 1
	return weather_dict

output = open('weather.txt','a')
# get a list of target date
for date in perdelta(date(2014, 2, 1), date(2014, 2, 18), timedelta(days=1)):
	# formate the date string
	date_string = str(date.year) + "/" + str(date.month) + "/" + str(date.day)
	print "processing weather data for " + date_string
	weather_query_url = build_query_url(date_string)
	html = send(weather_query_url)
	json_str = json.dumps(parse_html(html, date_string))
	output.write(json_str + "\n")
	time.sleep(0.5)