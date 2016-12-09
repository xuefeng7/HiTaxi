import json

facility_dict = json.load(open('Facilities.json','r'))
# {"region#119": 
# {"Great Outdoors": 0, "Home, Work, Other": 2, "Nightlife Spot": 0, "College & University": 0, "Food": 1, "Shop": 4, "Travel Spot": 1, 
#"Arts & Entertainment": 0}
output = open('trainset_2015_with_facility.txt','a+')
with open('trainset_2015_.txt') as tf:
		for trip in tf:
			trip = trip.split(",")
			region = trip[0]
			fac_lst = []
			for key in facility_dict["region#" + region].keys():
				fac_lst.append(facility_dict["region#" + region][key])
			trip = trip + fac_lst
			output.write(str(trip).replace('\'',"").replace('[',"").replace(']',"") + "\n")

# great_outdoor, home/work/other, nightlife_spot, college_university, food, shop, travel_spot, art_entertain