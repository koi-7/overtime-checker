import requests


class NotionOperator:
    def __init__(self):
        pass

    @classmethod
    def insert_record(self, notion_token, db_id, date, overtime):
        request_url = 'https://api.notion.com/v1/pages/'
        headers = {'Accept': 'application/json',
                   'Authorization': 'Bearer ' + notion_token,
                   'Content-Type': 'application/json; charset=UTF-8',
                   'Notion-Version': '2022-06-28'}
        json = {'parent': {'database_id': db_id},
                'properties': {'Date': {'title': [{'text': {'content': date}}]},
                               'Time': {'rich_text': [{'text': {'content': overtime}}]}}}

        requests.post(request_url, headers=headers, json=json)

    @classmethod
    def read_records(self, notion_token, db_url, month):
        pass
