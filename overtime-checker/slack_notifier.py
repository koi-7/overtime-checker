import requests


CHANNEL = '02_overtime-checker'


class SlackNotifier:
    def __init__(self):
        pass

    @classmethod
    def send_notify(self, slack_token, data_dict, sum_of_time):
        text = ''

        for date, time in data_dict.items():
            text = text + date.ljust(10) + time.rjust(7) + '\n'
        text = text + '-' * 17 + '\n'
        text = text + 'Total'.center(10) + sum_of_time.rjust(7)

        api_url = 'https://slack.com/api/chat.postMessage'
        headers = {'Authorization': 'Bearer ' + slack_token}
        data = {'channel': CHANNEL, 'text': text}
        requests.post(api_url, headers=headers, data=data)
