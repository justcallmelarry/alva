import json
import logging
import os
import random
import requests
import sys

argument = sys.argv[1] if len(sys.argv) > 1 else None


def post_slack(payload):
    response = requests.post(url, data=payload)
    logging.info(response.text)


with open(os.path.join(os.path.dirname(__file__), 'webhook.json'), 'r') as json_file:
    json_data = json.loads(json_file.read())
    url = json_data.get('slack_webhook')
    channel = json_data.get('channel')

with open(os.path.join(os.path.dirname(__file__), 'alva-settings.json'), 'r', encoding='utf-8') as messages_file:
    json_data = json.loads(messages_file.read())
    msg30 = []
    msg15 = []
    msg = []
    for message in json_data.get('msg30'):
        msg30.append(message)
    for message in json_data.get('msg15'):
        msg15.append(message)
    for message in json_data.get('msg'):
        msg.append(message)

payload_text = {
    'username': 'Alva',
    'icon_emoji': ':beers:',
    'channel': channel
}

if argument == 'func1':
    payload_text['text'] = random.choice(msg30)
elif argument == 'func2':
    payload_text['text'] = random.choice(msg15)
elif argument == 'func3':
    payload_text['text'] = random.choice(msg)
else:
    logging.error('faulty argument')
    sys.exit()

post_slack(json.dumps(payload_text))
