#!/usr/bin/env python3
# coding: utf-8


import datetime
import os

from .functions import *
from .calendar_reader import *
from .notion_operator import *


MAIN_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(MAIN_DIR, '../data/')
CREDENTIALS_PATH = os.path.join(DATA_DIR, 'credentials.json')
GOOGLE_TOKEN_PATH = os.path.join(DATA_DIR, 'token.json')
NOTION_TOKEN_PATH = os.path.join(DATA_DIR, 'notion_token')
DB_URL_PATH = os.path.join(DATA_DIR, 'db_url.txt')


def main():
    creds = CalendarReader.get_credentials(CREDENTIALS_PATH, GOOGLE_TOKEN_PATH)
    yesterday = str(datetime.datetime.today().date() - datetime.timedelta(1))
    overtime = CalendarReader.get_overtime_yesterday(creds, yesterday)

    with open(NOTION_TOKEN_PATH, 'r') as f:
        notion_token = f.readline().rstrip('\n')
    db_id = Functions.url_to_dbid(DB_URL_PATH)
    yesterday = yesterday.replace('-', '/')

    if overtime:
        NotionOperator.insert_record(notion_token, db_id, yesterday, overtime)


if __name__ == '__main__':
    main()
