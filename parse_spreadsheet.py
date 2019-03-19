import csv
from datetime import datetime
from datetime import timedelta
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


with open('sleep_data.csv') as csvfile:
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

    hours = count_hours_of_sleep_by_day(nights)
    pp.pprint(hours)

    write_hours_per_day_to_csv(hours, 'sleep_hours_per_day.csv')


    import sys; sys.exit(0)
    for row in reader:
        if count % 3 == 0:
            headers.append(row)
            count += 1
        elif count % 3 == 1:
            timezone = pytz.timezone(row[1])
            start_time = datetime.strptime(row[2], '%d. %m. %Y %H:%M')
            end_time = datetime.strptime(row[3], '%d. %m. %Y %H:%M')
            row[2] = timezone.localize(start_time)
            row[3] = timezone.localize(end_time)
            row.pop(1)
            data.append(row)
            count += 1
        elif not two_rows:
            third_row.append(row)
            count = 0
        if row[0] == '1437540628043':
            # We've gotten to the part of the spreadsheet where they switch to a 2-row formula
            two_rows = True
    actual_headers = headers[0][0:15]
    actual_headers.pop(1)
    general_data = []
    general_data.append(actual_headers)
    for row in data:
        general_data.append(row[0:len(actual_headers)])

    with open('parsed_general_data.csv', 'w') as write_file:
        tz = pytz.timezone('America/New_York')
        writer = csv.writer(write_file)
        headers = True
        for row in general_data:
            if not headers:
                for i in [1, 2]:
                    row[i] = row[i].astimezone(tz=tz).strftime('%Y/%m/%d %H:%M')
            if headers:
                headers = False
            writer.writerow(row)

