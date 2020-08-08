import csv
import re

PATH = './apache.log'

# regex = re.compile(r'(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*\[(?P<date>.*)\].#
# *\"(?P<method>\D{1,6})\s(?P<path>.*.)\s[H].*\"\s\"(?P<agent>\D{1,}\/\S{1,})\s') # regex for user agent
regex = re.compile(r'(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*\[(?P<date>.*)\].'r'*\"(?P<method>\D{1,7})\s(?P<path>.*.)\s[H]') # noqa
RESULT = []
fields = [
    'ip',
    'date',
    'method',
    'path',
]


with open(PATH) as file:
    for index, line in enumerate(file):
        res = regex.search(line).groupdict()
        ip = res['ip']
        date = res['date']
        method = res['method']
        path = res['path']
        RESULT.append([ip, date, method, path])

with open('result.csv', 'w') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=';')
    csv_writer.writerow(fields)
    csv_writer.writerows(RESULT)
