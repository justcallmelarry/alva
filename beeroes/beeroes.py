import csv
import json
import logging
import requests
logging.basicConfig(filename='beer.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
webhook = ''
beeroes_names = []
payload = {'text': 'A big thank you to {} for the much appriciated beeroes run! :clap:'.format(beeroes_names)}


with open('beeroes.csv', 'r', encoding='utf-8') as beeroes:
    reader = csv.reader(beeroes)
    new_beeroes = list(reader)

with open('file.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    prev_beeroes = list(reader)

list_names = ([c for c in new_beeroes if c not in prev_beeroes])
logging.info(list_names)

for name in list_names:
    with open('file.csv', 'a', newline='', encoding='utf-8') as file:
            csv_writer = csv.writer(file, delimiter=';', quotechar='“')
            csv_writer.writerow(name)
            string_name = ''.join(name[0])
            logging.info(string_name)
            beeroes_names.append(string_name)
            logging.info(beeroes_names)

response = requests.post(webhook, data=json.dumps(
    {'text': 'A big thank you to {} for the much appriciated beeroes run! :clap:'.format(beeroes_names)}))
