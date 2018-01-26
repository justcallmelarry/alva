import csv
import json
import requests
webhook = 'https://hooks.slack.com/services/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'
beeroes_names = []
payload = {'text': 'A big thank you to {} for the much appriciated beeroes run! :clap:'.format(beeroes_names)}


with open('beeroes.csv', 'r', encoding='utf-8') as beeroes:
    reader = csv.reader(beeroes)
    new_beeroes = list(reader)

with open('file.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    prev_beeroes = list(reader)

list_names = ([c for c in new_beeroes if c not in prev_beeroes])
print(list_names)

for name in list_names:
    with open('file.csv', 'a', newline='', encoding='utf-8') as file:
            csv_writer = csv.writer(file, delimiter=';', quotechar='“')
            csv_writer.writerow(name)
            string_name = ''.join(name[0])
            print(string_name)
            beeroes_names.append(string_name)
            print(beeroes_names)

response = requests.post(webhook, data=json.dumps(
    {'text': 'A big thank you to {} for the much appriciated beeroes run! :clap:'.format(beeroes_names)}))
