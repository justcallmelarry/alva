import csv
import itertools
import json
import requests
webhook = ''
names = []

with open('file.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    prev_beeroes = list(reader)

with open('beeroes.csv', 'r', encoding='utf-8') as beeroes:
    for row in itertools.islice(beeroes, 1, None):
        if row[0] == row[0] in prev_beeroes:
            None
        else:
            names.append(row)
            with open('file.csv', 'a', newline='', encoding='utf-8') as file:
                csv_writer = csv.writer(file, delimiter=';', quotechar='“')
                csv_writer.writerow([row[0]])

response = requests.post(webhook, data=json.dumps(
    {f'A big thank you to {names} for the much appriciated beeroes run! :clap:'}))
