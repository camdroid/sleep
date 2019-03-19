import csv
from datetime import datetime
from datetime import timedelta
import pytz
import pdb
import pprint
import numpy as np
import matplotlib.pyplot as plt
from parse_spreadsheet import read_sleep_data_file

pp = pprint.PrettyPrinter()


TARGET_HOURS = 6.5


def read_in_file_for_sleep_debt():
    with open('sleep_hours_per_day.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        sleep_debt_sum = 0
        hours_slept = []
        sleep_debt = []
        sleep_debt_with_date = []
        headers = next(reader, None)
        for row in reader:
            date = datetime.strptime(row[0], '%Y-%m-%d')
            hours_slept_per_night = float(row[1])
            sleep_debt_per_night = hours_slept_per_night - TARGET_HOURS
            hours_slept.append(hours_slept_per_night)
            sleep_debt.append(sleep_debt_per_night)
            sleep_debt_sum += sleep_debt_per_night
            sleep_debt_with_date.append((date, sleep_debt_per_night))
            # pp.pprint('+ {:5.2f} = {:.2f} sleep debt'.format(
                      # sleep_debt_per_night, sleep_debt_sum))
        # pp.pprint('{} sleep debt'.format(sleep_debt_sum))
        return (sleep_debt, sleep_debt_with_date)

def get_sleep_debt_no_date():
    sleep_debt, _ = read_in_file_for_sleep_debt()
    return sleep_debt

def get_sleep_debt_with_date():
    _, sleep_debt_with_date = read_in_file_for_sleep_debt()
    return sleep_debt_with_date

# sleep_debt = get_sleep_debt_no_date()
# cumulative_sum = np.cumsum(sleep_debt)
#
# pp.pprint('Last month: {:.2f} hrs'.format(sum(sleep_debt[-30:])))
# pp.pprint('Last quarter: {:.2f} hrs'.format(sum(sleep_debt[-90:])))
# pp.pprint('Last half: {:.2f} hrs'.format(sum(sleep_debt[-180:])))
# pp.pprint('All time: {:.2f} hrs'.format(sum(sleep_debt)))

def plot_over_time_range(days):
    cumulative_sum = np.cumsum(sleep_debt[-days:])
    plt.plot(cumulative_sum[-days:])
    plt.scatter(range(len(hours_slept[-days:])), hours_slept[-days:])
    plt.plot(range(len(hours_slept[-days:])), [6.5]*len(hours_slept[-days:]))
    plt.show()

# plot_over_time_range(7)

def get_debt_through_date(end_date):
    sleep_debt = get_sleep_debt_with_date()
    trunc_sleep_debt = [datum for datum in sleep_debt
                        if datum[0] < end_date]
    cumulative_sleep_debt = sum([datum[1] for datum in trunc_sleep_debt])
    return cumulative_sleep_debt


def get_monthly_sleep_debt():
    end_of_feb = datetime.strptime('2019-03-01', '%Y-%m-%d')
    feb_sleep_debt = get_debt_through_date(end_of_feb)
    pp.pprint(feb_sleep_debt)

    end_of_march = datetime.strptime('2019-04-01', '%Y-%m-%d')
    march_sleep_debt = get_debt_through_date(end_of_march)
    pp.pprint(march_sleep_debt)


def avg_sleep_time():
    sleep_data = read_sleep_data_file()
    raise Exception("WIP")
    average_time_before_midnight = sum([
        night.start_time for night in sleep_data
        if not night.sleep_started_after_midnight()])
    average_time_after_midnight = sum([
        night.start_time for night in sleep_data
        if night.sleep_started_after_midnight()])
    pdb.set_trace()


avg_sleep_time()

pdb.set_trace()
pass
