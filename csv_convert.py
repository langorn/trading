import csv
import time
import datetime

month_dict = {
    'Jan':'01',
    'Feb':'02',
    'Mar':'03',
    'Apr':'04',
    'May':'05',
    'Jun':'06',
    'Jul':'07',
    'Aug':'08',
    'Sep':'09',
    'Oct':'10',
    'Nov':'11',
    'Dec':'12'
}
def readfile():
    csvfile = open('input.csv',encoding="utf-8")
    reader = csv.DictReader(csvfile)

    return reader

def writefile(data):
    csvfile = open('output.csv', 'w')
    writer = csv.writer(csvfile)
    writer.writerows(data)

def parse_data(data):
    table =[['Date Time', 'Open', 'High', 'Low', 'Close', 'Volume']]
    # print(data)
    for row in data:
        print(row)
        for key in row:
            if 'Date' in key:
                print(key)
                date_time = row[key]
                display_time = convert_date(date_time)

        if row['Vol.'].find('M'):
            volume = float(row['Vol.'][:-1]) * 10000000;
        if row['Vol.'].find('K'):
            volume = float(row['Vol.'][:-1]) * 1000;

        new_format = [display_time, row['Open'], row['High'], row['Low'], row['Price'], volume]
        table.append(new_format)
    return table

def convert_date(data):
    date_array = data.split()
    print(date_array)
    month = '';
    month_txt = date_array[0]
    day_txt = date_array[1][:-1]
    year_txt = date_array[2]

    if month_dict[month_txt]:
        month = month_dict[month_txt]
    full_date = year_txt + '-' + month + '-' + day_txt +' 00:00:00'
    full_date = datetime.datetime.strptime(full_date, "%Y-%m-%d %H:%M:%S")
    return full_date


share_data = readfile()
reconstruct = parse_data(share_data)
writefile(reconstruct)
