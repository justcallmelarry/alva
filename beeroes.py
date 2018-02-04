# -*- coding: utf-8 -*-
from alva import load_slack_settings, post_slack
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import json
import logging


def create_string(name_list):
    list_len = len(name_list)
    i = 1
    for name in name_list:
        if i == 1:
            name_string = '{}'.format(name)
        elif i == list_len:
            name_string = '{} & {}'.format(name_string, name)
        else:
            name_string = '{}, {}'.format(name_string, name)
        i += 1
    return name_string


def set_or_add(d, k, v):
    if k not in d:
        d[k] = v
    else:
        d[k] += v


logging.basicConfig(level=logging.WARNING, format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

if __name__ == '__main__':
    url, channel, payload_text = load_slack_settings()

    # google drive/sheets login-credentials-stuff
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)  # needs to be a service account
    client = gspread.authorize(creds)

    # get all beeroes that haven't been thanked before
    sheet = client.open('alva-beeroes').sheet1  # spreadsheet called alva-beeroes must be created and the service account invited by email to edit
    all_records = sheet.get_all_records()

    # now that we have ALL THE DATA, do some calculations
    old_beeroes = {}
    week_beeroes = []
    duplicate_check = {}
    virgins = []
    veterans = []
    i = 1
    for beero in all_records:
        i += 1
        bname = beero.get('Who')
        bdate = beero.get('When').replace('-', '')
        if beero.get('Cred') == 'X':
            set_or_add(old_beeroes, bname, 1)
            continue
        elif beero.get('Cred') == '-':
            continue
        else:
            if bname not in week_beeroes:
                week_beeroes.append(bname)
                if bdate not in duplicate_check:
                    duplicate_check[bdate] = []
                duplicate_check[bdate].append(bname)
            else:
                if bname in duplicate_check.get(bdate):
                    logging.warning('it seems that {} is trying to cheat!'.format(bname))
                    sheet.update_cell(i, 3, '-')
                    continue
                else:
                    if bdate not in duplicate_check:
                        duplicate_check[bdate] = []
                    duplicate_check[bdate].append(bname)
            sheet.update_cell(i, 3, 'X')
            if bname not in old_beeroes and bname not in virgins:
                virgins.append(bname)
            elif old_beeroes.get(bname) == 19:
                veterans.append(bname)

    # info printing
    logging.info('new beeroes: {}'.format(week_beeroes))
    logging.info('first time beeroes: {}'.format(virgins))

    # as long as there was someone doing a run this week, thank those brave souls
    if len(week_beeroes) > 0:
        string_thanks = 'A big thank you to {} for the much appriciated beer run! :clap:'.format(create_string(week_beeroes))

        # if there was someone who was on their first run, that certainly requires an extra shout out!
        if len(virgins) > 0:
            string_thanks = '{} And hey! It was also {}\'s first beer run! Yeeeeeey!'.format(string_thanks, create_string(virgins))

        # if someone has been on 20 runs total, that is both praise- and badge worthy
        if len(veterans) > 0:
            string_thanks = '{} ALSO WOW! {} {} been on 20 runs so far! This is the stuff legends are made of!'.format(string_thanks, create_string(veterans), 'has' if len(veterans) == 1 else 'have')
        payload_text['text'] = string_thanks

        # once all is well, post to slack
        post_slack(url, json.dumps(payload_text))
