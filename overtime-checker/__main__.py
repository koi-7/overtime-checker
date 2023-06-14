#!/usr/bin/env python3
# coding: utf-8


from __future__ import print_function
from datetime import timedelta, timezone
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


def main():
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
            overtime_total = datetime.timedelta(hours=0, minutes=0)
            format = '%Y-%m-%dT%H:%M:%S%z'
            for overtime_work in overtime_works:
                start_time = datetime.datetime.strptime(overtime_work['start'].get('dateTime'), format)
                end_time = datetime.datetime.strptime(overtime_work['end'].get('dateTime'), format)
                overtime_total = overtime_total + (end_time - start_time)

            total_sec = overtime_total.total_seconds()
            hour_message = '' if total_sec < 3600 else str(int(total_sec // 3600)) + '時間'
            print('今月の残業時間は' + hour_message + str(int(total_sec % 3600 // 60)) + '分です。')
        else:
            print('今月は残業していません。')

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()
