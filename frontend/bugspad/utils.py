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

    def bug_details(self, bug_id):
        resp = requests.get(self.base_url + '/bug/%s' % bug_id)
        bug_details = json.loads(resp.content)
        return bug_details

    def update_bug(self, bug_id, data):
        data['user'] = 'rtnpro@gmail.com'
        data['password'] = 'asdf'
        resp = requests.post(self.base_url + '/updatebug/', data=json.dumps(data))

    def get_bugs(self, product_id):
        '''
        API call to get all bugs in the form of a list for the given product_id
        Now using dummy values as such API doesnt exist
        '''
        return []

class Paginate():
    '''
    To render paginated view in bug list
    '''
    per_page = 20
    page = 1
    total_records = 0
    paging_max_end = 0

    def __init__(self, *args, **kwargs):
        self.per_page = kwargs.pop('per_page')
        self.page = kwargs.pop('page')
        self.total_records = kwargs.pop('total_records')

    def get_numbers(self):
        paging_start = 1 if (self.page <= 4) else (self.page - 3)
        paging_end = paging_start + 6

        self.paging_max_end = self.total_records / self.per_page + 1
        if paging_end > self.paging_max_end:
            paging_end = self.paging_max_end
            if paging_end - paging_start < 7 and paging_end >= 7:
                paging_start = paging_end - 6

        if self.paging_max_end <= 7:
            paging_start = 1
            paging_end = self.paging_max_end
        return paging_start, paging_end