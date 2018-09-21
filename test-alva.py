from alva import FriendlyNeighborhoodBeerBot
import ujson


def test(Alva: FriendlyNeighborhoodBeerBot, messages: list) -> None:
    for message in messages:
        Alva.payload_text['text'] = message
        response = Alva.post_slack(ujson.dumps(Alva.payload_text))
        assert response == 'ok', f'slack response failed: {response}'


if __name__ == '__main__':
    Alva = FriendlyNeighborhoodBeerBot()
    Alva.load_slack_settings()
    Alva.load_messages()
    for message in Alva.msg30, Alva.msg15, Alva.msg:
        test(Alva, message)
