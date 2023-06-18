#!/usr/bin/env python3
# coding: utf-8


from __future__ import print_function
from datetime import timedelta, timezone
import argparse
import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

MAIN_DIR = os.path.dirname(__file__)
AUTH_DIR = os.path.join(MAIN_DIR, '../auth/')
TOKEN_PATH = os.path.join(AUTH_DIR, 'token.json')
CREDENTIALS_PATH = os.path.join(AUTH_DIR, 'credentials.json')


def timedelta_to_yyyymmdd(timedelta):
    zero_paddming_month = '{:0>2}'.format(str(timedelta.month))
    zero_paddming_day = '{:0>2}'.format(str(timedelta.day))
    return str(timedelta.year) + '/' + zero_paddming_month + '/' + zero_paddming_day


def timedelta_to_hhmm(timedelta):
    total_seconds = timedelta.total_seconds()
    return str(int(total_seconds // 3600)) + ':' + '{:0>2}'.format(str(int(total_seconds % 3600 // 60)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', help='残業時間の詳細表示', action='store_true')
    args = parser.parse_args()

    creds = None

    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        beginning_of_the_month = datetime.date.today().replace(day=1).isoformat() + 'T00:00:00.000000+09:00'
        JST = timezone(timedelta(hours=+9), 'JST')
        now = datetime.datetime.now(JST).isoformat()

        result = service.events().list(calendarId="primary",
                                       q='残業',
                                       timeMin=beginning_of_the_month,
                                       timeMax=now,
                                       maxResults=50,
                                       singleEvents=True,
                                       orderBy='startTime').execute()
        overtime_works = result.get('items', [])

        if overtime_works:
            records = {}
            overtime_total = datetime.timedelta(hours=0, minutes=0)

            format = '%Y-%m-%dT%H:%M:%S%z'
            for overtime_work in overtime_works:
                start_time = datetime.datetime.strptime(overtime_work['start'].get('dateTime'), format)
                end_time = datetime.datetime.strptime(overtime_work['end'].get('dateTime'), format)

                overtime = end_time - start_time

                yyyymmdd = timedelta_to_yyyymmdd(start_time)

                if yyyymmdd in records:
                    records[yyyymmdd] = records[yyyymmdd] + overtime
                else:
                    records[yyyymmdd] = overtime

                overtime_total = overtime_total + overtime

            if args.verbose:
                for key, value in records.items():
                    print('{:<10}{:>7}'.format(key, timedelta_to_hhmm(value)))
                print('-' * 17)

            print('{:<10}{:>7}'.format('total', timedelta_to_hhmm(overtime_total)))
        else:
            print('今月は残業していません。')

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()
