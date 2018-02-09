from alva import load_slack_settings, load_messages, post_slack
import logging
import ujson


def test(messages):
    for message in messages:
        payload_text['text'] = message
        response = post_slack(url, ujson.dumps(payload_text))
        assert response == 'ok', logging.error('message error: {}'.format(message))


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    url, channel, payload_text = load_slack_settings()
    msg30, msg15, msg = load_messages()
    for message in msg30, msg15, msg:
        test(message)
