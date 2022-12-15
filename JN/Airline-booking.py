import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats


no_show_mu = 0.02434
no_show_sigma = 0.02436

def calc_no_show_rates(number):
    x = np.random.normal(no_show_mu, no_show_sigma, number)
    x = x[x > 0]
    plt.hist(x, bins=50)
    plt.title(str(x.size) + ' no-show rates')
    plt.show()
    return x.size

planes = calc_no_show_rates(100000)




