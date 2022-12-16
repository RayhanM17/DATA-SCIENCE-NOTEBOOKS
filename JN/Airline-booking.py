import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import scipy.stats as stats

#Important Variables
no_show_mu = 0.02434
no_show_sigma = 0.02436
plane_capacity = 30

#Generate no show rates
def gen_no_show_rates(number):
    x = np.random.normal(no_show_mu, no_show_sigma, number)
    x = x[x > 0]
    #plt.hist(x, bins=50)
    #plt.title(str(x.size) + ' no-show rates')
    #plt.show()
    return x

#Simulate attendance
def sim_shows(probs, passengers):
    sim_data = np.zeros((probs.size, 1000)) #2d array of zeros
    for i in range(0, probs.size):
        x = np.random.binomial(n=passengers,  # Number of passengers per trial
                                      p=1 - probs[i],  # show probability
                                      size=1000) # number of trials
        sim_data[i] = x
    return sim_data

# calculate bump rate, capacity percentage - WORK IN PROGRESS
def calc_bump(attendance):
    bump_rate = attendance[attendance > plane_capacity].size / (attendance.size * 1000)
    print(bump_rate)

# no_show_rates = gen_no_show_rates(100000)
# plane_attendance = sim_shows(no_show_rates, 34)
# calc_bump(plane_attendance)








