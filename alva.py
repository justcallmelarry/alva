import json
import logging
import os
import random
import sys
from datetime import datetime, date
from typing import Any

import requests


class FriendlyNeighborhoodBeerBot:
    def __init__(self) -> None:
        self.filepath = os.path.dirname(os.path.abspath(__file__))

    def post_slack(self, payload: Any) -> str:
        response = requests.post(self.url, data=payload)
        logging.info('slack response: {}'.format(response.text))
        return response.text

    def load_slack_settings(self) -> None:
        with open(os.path.join(self.filepath, 'conf', 'webhook.json'), 'r') as json_file:
            json_data = json.load(json_file)
            self.url = json_data.get('slack_webhook')
            self.channel = json_data.get('channel')
            self.payload_text = {
                'username': 'Alva',
                'icon_emoji': json_data.get('icon_emoji'),
                'channel': self.channel,
                "link_names": 1
            }

    @staticmethod
    def replace_variables(message: str) -> str:
        reps = [
            ('$weekday', datetime.now().strftime('%A'))
        ]
        for rep in reps:
            message = message.replace(rep[0], rep[1])
        return message

    def load_generic_settings(self) -> None:
        with open(
            os.path.join(self.filepath, 'conf', 'alva-settings.json'),
            'r',
            encoding='utf-8'
        ) as messages_file:
            json_data = json.load(messages_file)
            self.bank_holidays = json_data.get('bank_holidays', [])
            self.msg30: list = []
            self.msg15: list = []
            self.msg: list = []
            for message in json_data.get('msg', {}).get('30', []):
                self.msg30.append(self.replace_variables(message))
            for message in json_data.get('msg', {}).get('15', []):
                self.msg15.append(self.replace_variables(message))
            for message in json_data.get('msg', {}).get('0', []):
                self.msg.append(self.replace_variables(message))

    def run(self, argument: str) -> None:
        self.load_generic_settings()
        self.load_slack_settings()
        today = date.today()
        adhoc_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tools', '__adhoc__')
        adhoc = os.path.isfile(adhoc_filepath)
        run = False
        if adhoc:
            run = True
        elif today.weekday() == 4:
            if today.strftime('%Y-%m-%d') in self.bank_holidays:
                return
            else:
                run = True
        if not run:
            return
        arguments = {
            'func1': random.choice(self.msg30),
            'func2': random.choice(self.msg15),
            'func3': random.choice(self.msg)
        }
        self.payload_text['text'] = arguments.get(argument, None)
        if not self.payload_text['text']:
            logging.error('faulty argument, {}, {}'.format(argument, self.payload_text))
        else:
            self.post_slack(json.dumps(self.payload_text))
        if adhoc and argument == 'func3':
            os.remove(adhoc_filepath)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.WARNING,
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    try:
        argument = sys.argv[1]
    except Exception:
        argument = 'func3'

    Alva = FriendlyNeighborhoodBeerBot()
    Alva.run(argument)
