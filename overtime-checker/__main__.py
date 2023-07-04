#!/usr/bin/env python3
# coding: utf-8


import configparser
import datetime
import logging
import os
from logging import getLogger, FileHandler, Formatter

from .functions import *
from .calendar_reader import *
from .notion_operator import *
from .slack_notifier import *


MAIN_DIR = os.path.dirname(__file__)
CONFIG_PATH = os.path.join(MAIN_DIR, '../config/config.ini')
CREDENTIALS_PATH = os.path.join(MAIN_DIR, '../config/credentials.json')
GOOGLE_TOKEN_PATH = os.path.join(MAIN_DIR, '../config/google_token.json')
LOG_PATH = os.path.join(MAIN_DIR, '../logs/overtime-checker.log')


logger = getLogger(__name__)
logger.setLevel(logging.INFO)
handler = FileHandler(LOG_PATH)
fmt = Formatter('%(asctime)s %(levelname)-8s %(message)s')
handler.setFormatter(fmt)
logger.addHandler(handler)


def main():
    config_ini = configparser.ConfigParser()
    config_ini.read(CONFIG_PATH, encoding='utf-8')

    # Google 認証
    try:
        creds = CalendarReader.get_credentials(CREDENTIALS_PATH, GOOGLE_TOKEN_PATH)
    except:
        logger.error('Google 認証失敗')
        sys.exit(1)

    today = str(datetime.datetime.today().date())  # 今日の日付（yyyy-MM-dd）
    overtime = CalendarReader.get_overtime(creds, today)  # 残業時間（hh:mm）
    today = today.replace('-', '/')  ## yyyy-MM-dd -> yyyy/MM/dd

    # Notion トークン、DB ID 取得
    notion_token = config_ini['Notion']['token']
    notion_database_url = config_ini['Notion']['database_url']
    l = notion_database_url.split('/')
    notion_database_id = l[4].split('?')[0]

    # 残業時間があれば DB に記録
    if overtime:
        NotionOperator.insert_record(notion_token, notion_database_id, today, overtime)

    # 翌日の日付 yyyy/MM/dd の dd が '01' なら
    if str(datetime.datetime.today().date() + datetime.timedelta(1))[-2:] == '01':
        overtime_dict = NotionOperator.read_records(notion_token, notion_database_id, today[:-3])  # 残業日付・残業時間の辞書取得

        sum = Functions.sum_of_timelist(list(overtime_dict.values()))  # ひと月の合計残業時間取得

        # Slack トークン取得
        slack_token = config_ini['Slack']['token']

        # Slack で通知
        SlackNotifier.send_notify(slack_token, overtime_dict, sum)

    logger.info('正常終了')


if __name__ == '__main__':
    main()
