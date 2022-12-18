import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import scipy.stats as stats

#Important Variables
no_show_mu = 0.02434
no_show_sigma = 0.02436
plane_capacity = 217
ticket_price = 1016.94
max_compensation = 1550

#Generate no show rates
def gen_no_show_rates(number):
    x = np.random.normal(no_show_mu, no_show_sigma, number)
    x[x < 0] = 0
    #plt.hist(x, bins=50)
    #plt.title(str(number) + ' no-show rates')
    #plt.show()
    return x

#Simulate attendance
def sim_shows(probs, booked, trials):
    sim_data = np.zeros((probs.size, trials)) #2d array of zeros
    for i in range(0, probs.size):
        x = np.random.binomial(n=booked,  # Number of passengers booked per trial
                                      p=1 - probs[i],  # show probability
                                      size=trials) # number of trials
        sim_data[i] = x
    return sim_data

# number of overbooked flights, total bumps, & bump rate
def calc_bump(attendance, booked):
    x = attendance[attendance > plane_capacity].size
    y = (attendance[attendance > plane_capacity] - plane_capacity).sum()
    z = y / (attendance.size * booked)
    return x, y, z

# calculate compensation, opportunity lost, capacity
def calc_profit(attendance, bumps):
    x = bumps * max_compensation
    y = (abs(attendance[attendance < plane_capacity] - plane_capacity)).sum() * ticket_price
    attendance[attendance > plane_capacity] = plane_capacity
    z = (attendance.sum() / (attendance.size * plane_capacity)).round(4)
    return x, y, z

# MASTER SIM - WORK IN PROGRESS
def overbooking_sim():
    sim_data = pd.Dataframe(
        {},
    )


no_show_rates = gen_no_show_rates(10000)
plane_attendance = sim_shows(no_show_rates, 220, 1000)
overbooked_flights, total_bumps, bump_rate = calc_bump(plane_attendance, 220)
print(calc_profit(plane_attendance, total_bumps))