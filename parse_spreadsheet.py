import csv
from datetime import datetime
from datetime import timedelta
import argparse
import pytz
import pprint
import night
import pdb


pp = pprint.PrettyPrinter()


def count_hours_of_sleep_by_day(nights):
    sleep_duration = {}
    for night in nights:
        target_date = night.start_time.date()
        if night.sleep_started_after_midnight():
            target_date -= timedelta(days=1)
        sleep_duration.setdefault(target_date, []).append(night.duration)

    # Feels like there's a way to do with with setdefault that I
    # can't figure out right now
    for (date, values) in sleep_duration.items():
        sleep_duration[date] = sum(values)
    return sleep_duration

def write_hours_per_day_to_csv(data, filename):
    # Using this to export data for my dashboard project
    # https://github.com/camdroid/dashboard
    with open(filename, 'w') as write_file:
        writer = csv.writer(write_file)
        writer.writerow(['Date','Hours'])
        for (date, duration) in data.items():
            output_row = [date.strftime('%Y-%m-%d'), duration]
            writer.writerow(output_row)

def read_sleep_data_file(filename=None):
    if filename is None:
        filename = 'sleep_data.csv'
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        headers = []
        data = []
        third_row = []
        count = 0
        two_rows = False

        slice_general = 6
        rows = []
        nights = []
        for i, row in enumerate(reader):
            row = row[:slice_general]
            if row[0] == 'Id':
                if len(rows) == 3:
                    n = night.read_3_lines_from_csv(rows)
                    nights.append(n)
                    rows = []
                elif len(rows) == 2:
                    print('Only reading 3-line nights right now')
                    rows = []
            rows.append(row)
    return nights


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', required=False, default=None)
    args = parser.parse_args()
    nights = read_sleep_data_file(args.filename)
    hours = count_hours_of_sleep_by_day(nights)
    pp.pprint(hours)
    write_hours_per_day_to_csv(hours, 'sleep_hours_per_day.csv')
