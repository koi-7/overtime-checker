import datetime


class Functions:
    def __init__(self):
        pass

    @classmethod
    def url_to_dbid(self, db_url_path):
        with open(db_url_path, 'r') as f:
            url =  f.readline().rstrip('\n')
        l = url.split('/')
        return l[4].split('?')[0]

    @classmethod
    def sum_of_timelist(self, timelist):
        sum = datetime.timedelta(0)
        for time in timelist:
            hours, minutes = map(int, time.split(":"))
            time = datetime.timedelta(hours=hours, minutes=minutes)
            sum = sum + time

        total_seconds = sum.total_seconds()
        return str(int(total_seconds // 3600)) + ':' + '{:0>2}'.format(str(int(total_seconds % 3600 // 60)))
