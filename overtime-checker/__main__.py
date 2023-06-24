#!/usr/bin/env python3
# coding: utf-8


import datetime
import os

from .functions import *
from .calendar_reader import *
from .notion_operator import *
from .slack_notifier import *


MAIN_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(MAIN_DIR, '../data/')
CREDENTIALS_PATH = os.path.join(DATA_DIR, 'credentials.json')
GOOGLE_TOKEN_PATH = os.path.join(DATA_DIR, 'token.json')
NOTION_TOKEN_PATH = os.path.join(DATA_DIR, 'notion_token')
DB_URL_PATH = os.path.join(DATA_DIR, 'db_url.txt')
SLACK_TOKEN_PATH = os.path.join(DATA_DIR, 'slack_token')


def main():
    # Google 認証
    creds = CalendarReader.get_credentials(CREDENTIALS_PATH, GOOGLE_TOKEN_PATH)

    yesterday = str(datetime.datetime.today().date() - datetime.timedelta(1))  # 昨日の日付（yyyy-MM-dd）
    overtime = CalendarReader.get_overtime_yesterday(creds, yesterday)  # 残業時間（hh:mm）

    # Notion トークン、DB ID 取得
    with open(NOTION_TOKEN_PATH, 'r') as f:
        notion_token = f.readline().rstrip('\n')
    db_id = Functions.url_to_dbid(DB_URL_PATH)

    yesterday = yesterday.replace('-', '/')  ## yyyy-MM-dd -> yyyy/MM/dd

    # 残業時間があれば DB に記録
    if overtime:
        NotionOperator.insert_record(notion_token, db_id, yesterday, overtime)

    # 日付 yyyy/MM/dd の dd が '01' なら
    if str(datetime.datetime.today().date())[-2:] == '01':
        previous_month = yesterday[:-3]  # 先月の yyyy/MM 取得
        overtime_dict = NotionOperator.read_records(notion_token, db_id, previous_month)  # 残業日付・残業時間の辞書取得

        sum = Functions.sum_of_timelist(list(overtime_dict.values()))  # ひと月の合計残業時間取得

        # Slack トークン取得
        with open(SLACK_TOKEN_PATH, 'r') as f:
            slack_token = f.readline().rstrip('\n')

        # Slack で通知
        SlackNotifier.send_notify(slack_token, overtime_dict, sum)


if __name__ == '__main__':
    main()
