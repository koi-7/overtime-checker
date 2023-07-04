import sys

import requests


class NotionOperator:
    def __init__(self):
        pass

    @classmethod
    def insert_record(self, notion_token, notion_database_id, date, overtime):
        request_url = 'https://api.notion.com/v1/pages/'
        headers = {'Accept': 'application/json',
                   'Authorization': 'Bearer ' + notion_token,
                   'Content-Type': 'application/json; charset=UTF-8',
                   'Notion-Version': '2022-06-28'}
        json = {'parent': {'database_id': notion_database_id},
                'properties': {'Date': {'title': [{'text': {'content': date}}]},
                               'Time': {'rich_text': [{'text': {'content': overtime}}]}}}

        requests.post(request_url, headers=headers, json=json)

    @classmethod
    def read_records(self, notion_token, notion_database_id, year_month):
        req_url = 'https://api.notion.com/v1/databases/' + notion_database_id + '/query'
        headers = {'Authorization': 'Bearer ' + notion_token,
                   'Content-Type': 'application/json; charset=UTF-8',
                   'Notion-Version': '2022-06-28'}

        try:
            response = requests.post(url=req_url, headers=headers)
            response.raise_for_status()
        except Exception:
            print('Error: DB URL or token is invalid.')
            sys.exit(1)
        json_data = response.json()
        results = json_data.get('results')

        try:
            overtime_of_month = {}
            for result in results:
                date = result['properties']['Date']['title'][0]['text']['content']
                time = result['properties']['Time']['rich_text'][0]['text']['content']
                if date[:-3] == year_month:
                    overtime_of_month[date] = time
            overtime_of_month = dict(sorted(overtime_of_month.items()))
        except Exception:
            print('Error: Name or type of column is wrong.')
            sys.exit(1)

        return overtime_of_month
