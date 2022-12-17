import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import scipy.stats as stats

#Important Variables
no_show_mu = 0.02434
no_show_sigma = 0.02436
plane_capacity = 217
ticket_price = 1016.94

#Generate no show rates
def gen_no_show_rates(number):
    x = np.random.normal(no_show_mu, no_show_sigma, number)
    x[x < 0] = 0
    #plt.hist(x, bins=50)
    #plt.title(str(number) + ' no-show rates')
    #plt.show()
    return x

#Simulate attendance
def sim_shows(probs, passengers, trials):
    sim_data = np.zeros((probs.size, trials)) #2d array of zeros
    for i in range(0, probs.size):
        x = np.random.binomial(n=passengers,  # Number of passengers per trial
                                      p=1 - probs[i],  # show probability
                                      size=trials) # number of trials
        sim_data[i] = x
    return sim_data

# number of overbooked flights, total bumps, & bump rate
def calc_bump(attendance, passengers):
    x = attendance[attendance > plane_capacity].size
    y = (attendance[attendance > plane_capacity] - plane_capacity).sum()
    z = y / (attendance.size * passengers)
    return x, y, z

# calculate total compesation, profit
def calc_profit(attendance, bumps):





no_show_rates = gen_no_show_rates(10000)
plane_attendance = sim_shows(no_show_rates, 34, 1000)
overbooked_flights, total_bumps, bump_rate = calc_bump(plane_attendance, 34)








