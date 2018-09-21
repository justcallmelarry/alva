from datetime import datetime
from typing import Any
import logging
import os
import random
import requests
import sys
import ujson


def post_slack(url: str, payload: Any) -> str:
    response = requests.post(url, data=payload)
    logging.info('slack response: {}'.format(response.text))
    return response.text


def load_slack_settings() -> tuple:
    with open(os.path.join(os.path.dirname(__file__), 'webhook.json'), 'r') as json_file:
        json_data = ujson.loads(json_file.read())
        url = json_data.get('slack_webhook')
        channel = json_data.get('channel')
        payload_text = {
            'username': 'Alva',
            'icon_emoji': ':beers:',
            'channel': channel,
            "link_names": 1
        }
        return url, channel, payload_text


def replace_variables(message: str) -> str:
    reps = [
        ('$weekday', datetime.now().strftime('%A'))
    ]
    for rep in reps:
        message = message.replace(rep[0], rep[1])
    return message


def load_messages() -> tuple:
    with open(os.path.join(os.path.dirname(__file__), 'alva-settings.json'), 'r', encoding='utf-8') as messages_file:
        json_data = ujson.loads(messages_file.read())
        msg30 = []
        msg15 = []
        msg = []
        for message in json_data.get('msg30'):
            msg30.append(replace_variables(message))
        for message in json_data.get('msg15'):
            msg15.append(replace_variables(message))
        for message in json_data.get('msg'):
            msg.append(replace_variables(message))
        return msg30, msg15, msg


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING, format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    try:
        argument = sys.argv[1]
    except Exception:
        argument = 'func3'
    url, channel, payload_text = load_slack_settings()
    msg30, msg15, msg = load_messages()

    arguments = {
        'func1': random.choice(msg30),
        'func2': random.choice(msg15),
        'func3': random.choice(msg)
    }
    payload_text['text'] = arguments.get(argument, None)
    if not payload_text['text']:
        logging.error('faulty argument, {}, {}'.format(argument, payload_text))
    else:
        post_slack(url, ujson.dumps(payload_text))
