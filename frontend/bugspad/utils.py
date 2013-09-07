import requests
import json


class BugspadBackendAPI(object):

    def __init__(self, base_url='http://127.0.0.1:9998'):
        self.base_url = base_url

    def create_bug(self, data):
        data['user'] = 'rtnpro@gmail.com'
        data['password'] = 'asdf'
        resp = requests.post(self.base_url + '/bug/', data=json.dumps(data))
        return int(resp.content)

