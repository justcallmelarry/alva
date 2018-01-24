# post to slack everytime a new excel finle with beer releases on systembolaget is avaliable during 2018
# -*- coding: utf-8 -*-
import csv
import json
import logging
import requests
logging.basicConfig(filename='systemet.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
systembolaget = 'https://www.systembolaget.se/fakta-och-nyheter/nyheter-i-sortimentet/lanseringar/'
url = ''  # input slack webhook
release_dates = ['19 jan', '2 feb', '16 feb', '2 mars', '16 mars', '6 april', '20 april', '4 maj', '18 maj', '8 juni', '6 juli', '3 aug', '17 aug', '7 sep', '21 sep', '5 okt', '19 okt', '2 nov', '16 nov', '7 dec']

with open('sma_partier.csv', 'r', encoding='utf-8') as csv_file:
    reader = csv.reader(csv_file)
    prev_dates = list(reader)

response = requests.get(systembolaget)

for string in release_dates:
    logging.info('små partier {}'.format(string))
    if 'små partier {}'.format(string) in response.text:
        shall_write = False
        if any(string in s for s in prev_dates):
            logging.info('No new releases')
        else:
            shall_write = True
            if shall_write is True:
                with open('sma_partier.csv', 'a', newline='', encoding='utf-8') as csv_file:
                    csv_writer = csv.writer(csv_file, delimiter=';', quotechar='“')
                    csv_writer.writerow([string])
                payload = {'text': 'Nu finns det en ny excel med små partier på Systembolaget den {}! Se länk här: {}'.format(string, systembolaget)}
                res = requests.post(url, data=json.dumps(payload))
                logging.info(res.text)
    else:
        logging.info('No matches')
