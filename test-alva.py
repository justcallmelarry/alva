from alva import FriendlyNeighborhoodBeerBot
import logging
import ujson


def test(Alva: FriendlyNeighborhoodBeerBot, messages: list) -> None:
    for message in messages:
        Alva.payload_text['text'] = message
        response = Alva.post_slack(ujson.dumps(Alva.payload_text))
        assert response == 'ok', logging.error(
            'message error: {}'.format(message)
        )


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    Alva = FriendlyNeighborhoodBeerBot()
    Alva.load_slack_settings()
    Alva.load_messages()
    for message in Alva.msg30, Alva.msg15, Alva.msg:
        test(Alva, message)
