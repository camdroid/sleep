import csv
from datetime import datetime
from datetime import timedelta
import pytz
import pdb
import pprint
import numpy as np
import matplotlib.pyplot as plt

pp = pprint.PrettyPrinter()


TARGET_HOURS = 6.5


with open('sleep_hours_per_day.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    sleep_debt_sum = 0
    hours_slept = []
    sleep_debt = []
    headers = next(reader, None)
    for row in reader:
        hours_slept_per_night = float(row[1])
        sleep_debt_per_night = hours_slept_per_night - TARGET_HOURS
        hours_slept.append(hours_slept_per_night)
        sleep_debt.append(sleep_debt_per_night)
        sleep_debt_sum += sleep_debt_per_night
        pp.pprint('+ {:5.2f} = {:.2f} sleep debt'.format(
                  sleep_debt_per_night, sleep_debt_sum))
    pp.pprint('{} sleep debt'.format(sleep_debt_sum))

cumulative_sum = np.cumsum(sleep_debt)

pp.pprint('Last month: {:.2f} hrs'.format(sum(sleep_debt[-30:])))
pp.pprint('Last quarter: {:.2f} hrs'.format(sum(sleep_debt[-90:])))
pp.pprint('Last half: {:.2f} hrs'.format(sum(sleep_debt[-180:])))
pp.pprint('All time: {:.2f} hrs'.format(sum(sleep_debt)))

def plot_over_time_range(days):
    cumulative_sum = np.cumsum(sleep_debt[-days:])
    plt.plot(cumulative_sum[-days:])
    plt.scatter(range(len(hours_slept[-days:])), hours_slept[-days:])
    plt.plot(range(len(hours_slept[-days:])), [6.5]*len(hours_slept[-days:]))
    plt.show()

plot_over_time_range(7)
