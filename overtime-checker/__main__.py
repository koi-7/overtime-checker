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
GOOGLE_TOKEN_PATH = os.path.join(DATA_DIR, 'google_token.json')
NOTION_TOKEN_PATH = os.path.join(DATA_DIR, 'notion_token')
DB_URL_PATH = os.path.join(DATA_DIR, 'database_url')
SLACK_TOKEN_PATH = os.path.join(DATA_DIR, 'slack_token')


def main():
    # Google 認証
    creds = CalendarReader.get_credentials(CREDENTIALS_PATH, GOOGLE_TOKEN_PATH)

    today = str(datetime.datetime.today().date())  # 今日の日付（yyyy-MM-dd）
    overtime = CalendarReader.get_overtime(creds, today)  # 残業時間（hh:mm）

    # Notion トークン、DB ID 取得
    with open(NOTION_TOKEN_PATH, 'r') as f:
        notion_token = f.readline().rstrip('\n')
    database_id = Functions.url_to_dbid(DB_URL_PATH)

    today = today.replace('-', '/')  ## yyyy-MM-dd -> yyyy/MM/dd

    # 残業時間があれば DB に記録
    if overtime:
        NotionOperator.insert_record(notion_token, database_id, today, overtime)

    # 翌日の日付 yyyy/MM/dd の dd が '01' なら
    if str(datetime.datetime.today().date() + datetime.timedelta(1))[-2:] == '01':
        overtime_dict = NotionOperator.read_records(notion_token, database_id, today[:-3])  # 残業日付・残業時間の辞書取得

        sum = Functions.sum_of_timelist(list(overtime_dict.values()))  # ひと月の合計残業時間取得

        # Slack トークン取得
        with open(SLACK_TOKEN_PATH, 'r') as f:
            slack_token = f.readline().rstrip('\n')

        # Slack で通知
        SlackNotifier.send_notify(slack_token, overtime_dict, sum)


if __name__ == '__main__':
    main()
