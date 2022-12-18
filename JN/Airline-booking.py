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

# number of overflow flights, total bumps, & bump rate
def calc_bump(attendance, booked):
    x = attendance[attendance > plane_capacity].size
    y = (attendance[attendance > plane_capacity] - plane_capacity).sum()
    z = y / (attendance.size * booked)
    return x, y, z

# calculate compensation, empty seats, opportunity lost, capacity
def calc_profit(attendance, bumps):
    w = bumps * max_compensation
    x = (abs(attendance[attendance < plane_capacity] - plane_capacity)).sum()
    y = x * ticket_price
    attendance[attendance > plane_capacity] = plane_capacity
    z = (attendance.sum() / (attendance.size * plane_capacity)).round(4)
    return w, x, y, z

# MASTER SIM - WORK IN PROGRESS
def overbooking_sim(data_points, runs):
    sim_data = pd.DataFrame(
        {},
        columns=np.arange(
            (1/plane_capacity), #start
            (data_points/plane_capacity), #stop
            (1/plane_capacity)), #step
        index=[
            'overflowed flights',
            'total bumps',
            'bump rate',
            'total compensation',
            'empty seats',
            'opportunity lost',
            'plane capacity']
    )
    no_show_rates = gen_no_show_rates(int(runs * 0.001))
    for i in range(1, 21):
        # calculate data
        plane_attendance = sim_shows(no_show_rates, plane_capacity + i, int(runs * 0.0001))
        overflowed_flights, bumps, bump_rate = calc_bump(plane_attendance, plane_capacity + i)
        total_comp, empty_seats, opportunity_lost, capacity = calc_profit(plane_attendance, bumps)

        # store data
        sim_data.loc[sim_data.index[0], sim_data.columns[i - 1]] = overflowed_flights
        sim_data.loc[sim_data.index[1], sim_data.columns[i - 1]] = bumps
        sim_data.loc[sim_data.index[2], sim_data.columns[i - 1]] = bump_rate
        sim_data.loc[sim_data.index[3], sim_data.columns[i - 1]] = total_comp
        sim_data.loc[sim_data.index[4], sim_data.columns[i - 1]] = empty_seats
        sim_data.loc[sim_data.index[5], sim_data.columns[i - 1]] = opportunity_lost
        sim_data.loc[sim_data.index[6], sim_data.columns[i - 1]] = capacity

    return sim_data



#no_show_rates = gen_no_show_rates(10000)
#plane_attendance = sim_shows(no_show_rates, 218, 1000)
#overflow_flights, total_bumps, bump_rate = calc_bump(plane_attendance, 218)
# total_comp, empty_seats, opportunity_lost, capacity = calc_profit(plane_attendance, total_bumps)
print(overbooking_sim(20, 10000000))
