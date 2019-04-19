# coding: utf-8
from alva import FriendlyNeighborhoodBeerBot
import json
import logging
import os
import pygsheets


def create_string(name_list: list) -> str:
    name_string = ''
    for i, name in enumerate(name_list, start=1):
        if not name or name == '':
            continue
        if name_string is None:
            name_string = '@{}'.format(name)
        elif i == len(name_list):
            name_string = '{} & @{}'.format(name_string, name)
        else:
            name_string = '{}, @{}'.format(name_string, name)
    return name_string


def set_or_add(d: dict, k: str, v: int) -> None:
    if k not in d:
        d[k] = v
    else:
        d[k] += v


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.WARNING,
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # google drive/sheets login-credentials-stuff
    client = pygsheets.authorize(
        service_file=os.path.join(
            os.path.dirname(__file__),
            'conf',
            'client_secret.json'
        )
    )

    # get all beeroes that haven't been thanked before
    # spreadsheet called alva-beeroes must be created
    # and the service account invited by email to edit
    sheet = client.open('alva-beeroes').sheet1
    all_records = sheet.get_all_records()

    # now that we have ALL THE DATA, do some calculations
    old_beeroes: dict = {}
    week_beeroes: list = []
    duplicate_check: dict = {}
    virgins: list = []
    veterans: list = []
    for i, beero in enumerate(all_records, start=2):
        try:
            bname = beero.get('Who')
            if bname is None or bname == '' or beero.get('Cred') == '-':
                continue
            bdate = beero.get('When').replace('-', '')
            if beero.get('Cred') == 'X':
                set_or_add(old_beeroes, bname, 1)
                continue
            else:
                if bname not in week_beeroes:
                    week_beeroes.append(bname)
                    if bdate not in duplicate_check:
                        duplicate_check[bdate] = []
                    duplicate_check[bdate].append(bname)
                else:
                    if bname in duplicate_check.get(bdate, []):
                        logging.warning(
                            'it seems that {} is trying to cheat!'.format(bname)
                        )
                        # update column C of the current row
                        sheet.update_cell('C{}'.format(i), '-')
                        continue
                    else:
                        if bdate not in duplicate_check:
                            duplicate_check[bdate] = []
                        duplicate_check[bdate].append(bname)
                # update column C of the current row
                sheet.update_cell('C{}'.format(i), 'X')
                if bname not in old_beeroes and bname not in virgins:
                    virgins.append(bname)
                elif old_beeroes.get(bname) == 19:
                    veterans.append(bname)
        except Exception as e:
            logging.warning('beero-problem: {}'.format(e))

    # info printing
    logging.info('new beeroes: {}'.format(week_beeroes))
    logging.info('first time beeroes: {}'.format(virgins))

    # as long as there was someone doing a run this week, thank those brave souls
    if len(week_beeroes) > 0:
        string_thanks = 'A big thank you to {} for the much appriciated beer run! :clap:'.format(
            create_string(week_beeroes)
        )

        # if there was someone who was on their first run, that certainly requires an extra shout out!
        if len(virgins) > 0:
            string_thanks += ' And hey! It was also {}\'s first beer run this year! Yeeeeeey!'.format(
                create_string(virgins)
            )

        # if someone has been on 20 runs total, that is both praise- and badge worthy
        if len(veterans) > 0:
            string_thanks += ' ALSO WOW! {} {} been on 20 runs so far! This is the stuff legends are made of!'.format(
                create_string(veterans),
                'has' if len(veterans) == 1 else 'have'
            )
        Alva = FriendlyNeighborhoodBeerBot()
        Alva.load_slack_settings()
        Alva.payload_text['text'] = string_thanks

        # once all is well, post to slack
        Alva.post_slack(json.dumps(Alva.payload_text))
