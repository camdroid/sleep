import csv
from datetime import timedelta
import argparse
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
        # Sum values just in case there are multiple entries
        # for a single day
        sleep_duration[date] = sum(values)
    return sleep_duration


def write_hours_per_day_to_csv(data, filename):
    # Using this to export data for my dashboard project
    # https://github.com/camdroid/dashboard
    with open(filename, 'w') as write_file:
        writer = csv.writer(write_file)
        writer.writerow(['Date','Hours'])
        output_rows = []
        for (date, duration) in data.items():
            output_row = [date.strftime('%Y-%m-%d'), duration]
            output_rows.append(output_row)
        # Sort by date to make debugging easier
        # TODO There's probably a more Pythonic way to do this whole function
        output_rows.sort()
        for output_row in output_rows:
            writer.writerow(output_row)
    pp.pprint('Wrote output to {}'.format(filename))


def get_next_chunk(all_lines):
    chunk = []
    for row in all_lines:
        if row[0] == 'Id':
            ret = chunk
            chunk = []
            yield ret
        chunk.append(row)
    yield chunk


def read_sleep_data_file(filename):
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        slice_general = 6
        rows = []
        nights = []

        rows = [row[:slice_general] for row in reader]
        nights = [night.read_lines_from_csv(chunk) for chunk in get_next_chunk(rows)]
    return [night for night in nights if night]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='raw_sleep_data.csv')
    parser.add_argument('--output', default='sleep_hours_per_day.csv')
    args = parser.parse_args()

    nights = read_sleep_data_file(args.input)
    hours = count_hours_of_sleep_by_day(nights)
    write_hours_per_day_to_csv(hours, args.output)
