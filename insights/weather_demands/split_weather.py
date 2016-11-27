import numpy as np
from scipy.stats import ttest_ind
from math import sqrt
import scipy.stats as stats
import scipy as sp
import pylab as pl
# 2014 average weather map
# ave_monthly_weather_dict = {
# 	"1":35,"2":38,"3":46,"4":61,"5":73,"6":80,
# 	"7":83,"8":82,"9":77,"10":66,"11":52,"12":45
# }

# # cold = open('2014_cold.txt', 'a+')
# # hot = open('2014_hot.txt', 'a+')
# # normal = open('2014_normal.txt', 'a+')

# # convert temperature from f to c
# def f2c(f):
# 	return ((f - 32) * 5 / 9)

# cold = np.zeros(325186)
# hot = np.zeros(8750)
# normal = np.zeros(2695976)

# cold_count = 0
# hot_count = 0
# normal_count = 0

# with open('trainset_2014.txt') as tf:
# 	for trip in tf:
# 		# determine winter or summer
# 		month = int(trip.split(",")[1].split("/")[0])
# 		temp = float(trip.split(",")[4])
# 		count = int(trip.split(",")[6])
# 		# winter
# 		if month is 12 or month is 1 or month is 2:
# 			# 7 celsisus degree lower, cold weather
# 			if f2c(ave_monthly_weather_dict[str(month)]) - f2c(temp) >= 4:
# 				#cold.write(trip)
# 				cold[cold_count] = count
# 				cold_count += 1
# 			else:
# 				#normal.write(trip)
# 				normal[normal_count] = count
# 				normal_count += 1
# 		elif month is 6 or month is 7 or month is 8:
# 			# 7 celsisus degree higher, hot weather
# 			if f2c(temp) - f2c(ave_monthly_weather_dict[str(month)]) >= 4:
# 				# hot.write(trip)
# 				hot[hot_count] = count
# 				hot_count += 1
# 			else:
# 				#normal.write(trip)
# 				normal[normal_count ] = count
# 				normal_count += 1
# 		else:
# 			normal[normal_count] = count
# 			normal_count += 1

# abnormal = np.append(cold, hot)

# print np.mean(abnormal), np.mean(normal)
# print np.std(abnormal), np.std(normal)

def two_sample_t_test(x, y):
	loop = 100
	while loop > 0:
		rrs_x = np.random.choice(x, 50)
		rrs_y = np.random.choice(y, 50)
		t, p = ttest_ind(rrs_x, rrs_y, equal_var=False)
		if p < 0.05:
			print(str(loop) + ": ttest_ind for h-c:            t = %g  p = %g" % (t, p)) 
		loop -= 1

# two_sample_t_test(hot, normal)
def cohen_d(x,y):
	mean_x = np.mean(x)
	mean_y = np.mean(y)
	var_x = np.var(x, ddof=1)
	var_y = np.var(y, ddof=1)
	s = sqrt( ( (x.size - 1)*var_x + (y.size - 1)*var_y ) / ( x.size + y.size ))

	# t = (mean_x - mean_y) / sqrt(((s)**2) * ((1/x.size)+(1/y.size)))
	# ci95_lb = abs(x - y) - (2 * sqrt(((s)**2) * ((1/x.size)+(1/y.size))))
	# ci95_ub = abs(x - y) + (2 * sqrt(((s)**2) * ((1/x.size)+(1/y.size))))
	d = ( mean_x - mean_y ) / s 
	return d

# # # 2-sample t-test for cold, hot
# # print "cold - hot: " + str(cohen_d(cold, hot))
# print "cold - hot: " + str(cohen_d_and_ci(cold, hot)) 
# # t, p = ttest_ind(cold, hot, equal_var=False)
# # print("ttest_ind for cold-hot:            t = %g  p = %g" % (t, p))
# # # 2-sample t-test for normal, cold
# # print "normal - cold: " + str(cohen_d(normal, cold))
# print "normal - cold: " + str(cohen_d_and_ci(normal, cold))
# # t, p = ttest_ind(cold, normal, equal_var=False)
# # print("ttest_ind for normal-cold:            t = %g  p = %g" % (t, p))
# # # 2-sample t-test for normal, hot
# # print "normal - hot: " + str(cohen_d(normal, hot))
# print "normal - hot: " + str(cohen_d_and_ci(normal, hot))
# # t, p = ttest_ind(normal, hot, equal_var=False)
# # print("ttest_ind for normal-hot:            t = %g  p = %g" % (t, p))
# # # 2-sample t-test for normal, hot+cold
# abnormal = np.append(cold, hot)
# # print "normal - abnormal: " + str(cohen_d(normal, abnormal))
# print "normal - abnormal: " + str(cohen_d_and_ci(normal, abnormal))
# # t, p = ttest_ind(normal, abnormal, equal_var=False)
# # print("ttest_ind for normal-abnormal:            t = %g  p = %g" % (t, p))
weather_cond = {
	"extreme": ["Chilly", 'Frigid', 'Cold', "HeavyRain", "HeavySnow", "Snow", 'Rain','LightFreezingRain', "LightRain", "LightSnow", 'Quitecool'],
	"nonextreme": ['ScatteredClouds', 'MostlyCloudy', 'PartlyCloudy', 'Clear', 'Overcast', 'Haze', 'Mild', 'Cool','Fog', 'Mist']
}

extreme_count = 0
nonextreme_count = 0
extreme = np.zeros(3029912)
nonextreme = np.zeros(3029912)

with open('trainset_2014.txt') as tf:
	for trip in tf:	

		cond = trip.split(",")[5].split('(')[1].replace(")","")
		count = int(trip.split(",")[6])
		
		if cond in weather_cond['extreme']:
			extreme[extreme_count] = count
			extreme_count += 1
		else:
			nonextreme[nonextreme_count] = count
			nonextreme_count += 1

extreme = extreme[extreme != 0]
nonextreme = nonextreme[nonextreme != 0]

print np.mean(extreme), np.mean(nonextreme)
print np.std(extreme), np.std(nonextreme)
print extreme.size, nonextreme.size

print "extreme - nonextreme: " + str(cohen_d(extreme, nonextreme))

loop = 100
while loop > 0:
	rrs_extreme = np.random.choice(extreme, 60)
	rrs_nonextreme = np.random.choice(nonextreme, 60)

	t, p = ttest_ind(rrs_extreme, rrs_nonextreme, equal_var=False)
	if p < 0.05:
		print(str(loop) + ": ttest_ind for e-n:            t = %g  p = %g" % (t, p)) 
	loop -= 1


