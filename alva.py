from datetime import datetime
from typing import Any
import logging
import os
import random
import requests
import sys
import ujson


class FriendlyNeighborhoodBeerBot:
    def __init__(self) -> None:
        self.filepath = os.path.dirname(os.path.abspath(__file__))

    def post_slack(self, payload: Any) -> str:
        response = requests.post(self.url, data=payload)
        logging.info('slack response: {}'.format(response.text))
        return response.text

    def load_slack_settings(self) -> None:
        with open(os.path.join(self.filepath, 'webhook.json'), 'r') as json_file:
            json_data = ujson.load(json_file)
            self.url = json_data.get('slack_webhook')
            self.channel = json_data.get('channel')
            self.payload_text = {
                'username': 'Alva',
                'icon_emoji': ':alva_whale:',
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

    def load_messages(self) -> None:
        with open(
            os.path.join(self.filepath, 'alva-settings.json'),
            'r',
            encoding='utf-8'
        ) as messages_file:
            json_data = ujson.load(messages_file)
            self.msg30: list = []
            self.msg15: list = []
            self.msg: list = []
            for message in json_data.get('msg30'):
                self.msg30.append(self.replace_variables(message))
            for message in json_data.get('msg15'):
                self.msg15.append(self.replace_variables(message))
            for message in json_data.get('msg'):
                self.msg.append(self.replace_variables(message))

    def run(self) -> None:
        self.load_slack_settings()
        self.load_messages()
        arguments = {
            'func1': random.choice(self.msg30),
            'func2': random.choice(self.msg15),
            'func3': random.choice(self.msg)
        }
        self.payload_text['text'] = arguments.get(argument, None)
        if not self.payload_text['text']:
            logging.error('faulty argument, {}, {}'.format(argument, self.payload_text))
        else:
            self.post_slack(ujson.dumps(self.payload_text))


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
    Alva.run()
