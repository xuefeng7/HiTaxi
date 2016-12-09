## This script is tring to fit possion distribution to the
## the demands
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.misc import factorial

### Training Set Generation
def read_count(set_name, SIZE):

	truth_vector = np.zeros(shape=(SIZE, ))
	# read in observation set
	with open(set_name) as tf:
		obser_count = 0
		for observation in tf:
			observation = observation.split(",")
			truth = int(observation[6].replace("\\","").replace("n",""))
	
	return truth_vector

def poisson(k, lamb):
    """poisson pdf, parameter lamb is the fit parameter"""
    return (lamb**k/factorial(k)) * np.exp(-lamb)

def negLogLikelihood(params, data):
    """ the negative log-Likelohood-Function"""
    lnl = - np.sum(np.log(poisson(data, params[0])))
    return lnl

SIZE = 3029912
# get count
data = read_count('trainset_2014_with_facility.txt', SIZE)
# minimize the negative log-Likelihood
result = minimize(negLogLikelihood,  # function to minimize
                  x0=np.ones(1),     # start value
                  args=(data,),      # additional arguments for function
                  method='Powell',   # minimization method, see docs
                  )
# result is a scipy optimize result object, the fit parameters 
# are stored in result.x
print(result)

# plot poisson-deviation with fitted parameter
x_plot = np.linspace(0, np.amax(data), np.amax(data))

plt.hist(data, bins=51, normed=True, color='#EE799F')
plt.plot(x_plot, poisson(x_plot, result.x), 'r-', lw=2)
plt.show()