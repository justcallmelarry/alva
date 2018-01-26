import csv
import json
import logging
import requests
logging.basicConfig(filename='beer.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
webhook = 'https://hooks.slack.com/services/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'


with open('beeroes.csv', 'r', encoding='utf-8') as beeroes:
    reader = csv.reader(beeroes)
    new_beeroes = [x.strip() for x in beeroes][1:]

with open('file.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    prev_beeroes = [x.strip() for x in file][1:]

list_names = new_beeroes[len(prev_beeroes):]
logging.info(list_names)

list_beeroes = ', '.join(list_names)

beeroe_virgin = [c for c in new_beeroes if c not in prev_beeroes]
logging.info(beeroe_virgin)

list_virgins = ', '.join(beeroe_virgin)


with open('file.csv', 'a', newline='', encoding='utf-8') as file:
    csv_writer = csv.writer(file, delimiter=';', quotechar='“')
    csv_writer.writerow(list_names)


if len(beeroe_virgin):
    response = requests.post(webhook, data=json.dumps(
        {'text': 'A big thank you to {} for the much appriciated beeroes run! :clap: Hey! It was also {} first beer run! Yeeeeeey!'.format(list_beeroes, list_virgins)}))
else:
    response = requests.post(webhook, data=json.dumps(
        {'text': 'A big thank you to {} for the much appriciated beeroes run! :clap:'.format(list_beeroes)}))
