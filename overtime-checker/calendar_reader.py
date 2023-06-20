from __future__ import print_function
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import datetime
import os
import sys


SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


class CalendarReader:
    def __init__(self):
        pass

    @classmethod
    def get_credentials(self, credentials_path, token_path):
        creds = None

        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
            with open(token_path, 'w') as token:
                token.write(creds.to_json())

        return creds

    @classmethod
    def get_overtime_yesterday(self, creds, date):
        try:
            service = build('calendar', 'v3', credentials=creds)

            start = date + 'T00:00:00.000000+09:00'
            end = date + 'T23:59:59.000000+09:00'

            result = service.events().list(calendarId="primary",
                                           q='残業',
                                           timeMin=start,
                                           timeMax=end,
                                           maxResults=10,
                                           singleEvents=True,
                                           orderBy='startTime').execute()

            overtime_works = result.get('items', [])

            if overtime_works:
                format = '%Y-%m-%dT%H:%M:%S%z'
                overtime = datetime.timedelta(0)

                for overtime_work in overtime_works:
                    overwork_start = datetime.datetime.strptime(overtime_work['start'].get('dateTime'), format)
                    overwork_end = datetime.datetime.strptime(overtime_work['end'].get('dateTime'), format)
                    overtime = overtime + (overwork_end - overwork_start)

                return str(overtime)[:-3]
            else:
                return '0'

        except HttpError as error:
            print('An error occurred: %s' % error)
            sys.exit(1)
