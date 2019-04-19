import json

from alva import FriendlyNeighborhoodBeerBot


def test(Alva: FriendlyNeighborhoodBeerBot, messages: list) -> None:
    for message in messages:
        Alva.payload_text['text'] = message
        response = Alva.post_slack(json.dumps(Alva.payload_text))
        assert response == 'ok', f'slack response failed: {response}'


if __name__ == '__main__':
    Alva = FriendlyNeighborhoodBeerBot()
    Alva.load_slack_settings()
    Alva.load_generic_settings()
    for message in Alva.msg30, Alva.msg15, Alva.msg:
        test(Alva, message)
