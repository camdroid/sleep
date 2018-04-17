import csv

with open('sleep_data.csv') as csvfile:
    reader = csv.reader(csvfile)
    headers = []
    data = []
    third_row = []
    count = 0
    two_rows = False
    for row in reader:
        if count % 3 == 0:
            headers.append(row)
            count += 1
        elif count % 3 == 1:
            data.append(row)
            count += 1
        elif not two_rows:
            third_row.append(row)
            count = 0
        if row[0] == '1437540628043':
            # We've gotten to the part of the spreadsheet where they switch to a 2-row formula
            two_rows = True
    actual_headers = headers[0][0:15]
    general_data = []
    general_data.append(actual_headers)
    for row in data:
        general_data.append(row[0:15])

    with open('parsed_general_data.csv', 'w') as write_file:
        writer = csv.writer(write_file)
        for row in general_data:
            writer.writerow(row)

