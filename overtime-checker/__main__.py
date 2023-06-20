#!/usr/bin/env python3
# coding: utf-8


import datetime
import os

from .calendar_reader import *


MAIN_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(MAIN_DIR, '../data/')
CREDENTIALS_PATH = os.path.join(DATA_DIR, 'credentials.json')
TOKEN_PATH = os.path.join(DATA_DIR, 'token.json')


def main():
    creds = CalendarReader.get_credentials(CREDENTIALS_PATH, TOKEN_PATH)
    yesterday = str(datetime.datetime.today().date() - datetime.timedelta(1))
    overtime = CalendarReader.get_overtime_yesterday(creds, yesterday)

    print(overtime)


if __name__ == '__main__':
    main()
