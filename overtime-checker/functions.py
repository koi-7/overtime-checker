class Functions:
    def __init__(self):
        pass

    @classmethod
    def url_to_dbid(self, db_url_path):
        with open(db_url_path, 'r') as f:
            url =  f.readline().rstrip('\n')
        l = url.split('/')
        return l[4].split('?')[0]
