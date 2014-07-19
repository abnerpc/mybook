# coding: utf-8

import os
import unittest
import json
from os import path
from mybook import mybookapp


base_path = path.dirname(path.realpath(__file__))
cfg_path = path.join(base_path, 'mybook', 'config', 'testing.py')
os.environ['TODO_SETTINGS'] = cfg_path
app = mybookapp.create_app()


class MyAppTestCase(unittest.TestCase):

    def test_config_settings(self):
        config = app.config
        assert config['DATABASE'] == 'sqlite:///test.db'
        assert config['TESTING']
        assert config['DEBUG']


class ApiPostTestCase(unittest.TestCase):

    def setUp(self):
        mybookapp.people.delete()
        self.client = app.test_client()

    def tearDown(self):
        mybookapp.people.delete()

    def test_send_post_without_id(self):
        response = self.client.post(
            '/api/person/')
        assert response.status_code == 400

    def test_create_person_by_username(self):
        response = self.client.post(
            '/api/person/',
            data={'facebookId': 'abnerpc'})
        assert response.status_code == 201

    def test_create_person_by_id(self):
        response = self.client.post(
            '/api/person/',
            data={'facebookId': '100000095239174'})
        assert response.status_code == 201

    def test_create_invalid_id(self):
        response = self.client.post(
            '/api/person/',
            data={'facebookId': '1213dddd2222madfn71212@#@$wfwf3244fff@@@'})
        assert response.status_code == 403

    def test_create_user_same_id(self):
        response1 = self.client.post(
            '/api/person/',
            data={'facebookId': 'abnerpc'})
        response2 = self.client.post(
            '/api/person/',
            data={'facebookId': 'abnerpc'})
        assert response1.status_code == 201
        assert response2.status_code == 403


class ApiGetTestCase(unittest.TestCase):

    def setUp(self):
        self.info_rows = 1
        self.inserted_rows = 5
        self.total_rows = self.info_rows + self.inserted_rows
        rows = [dict(username='abnerpc')] * self.inserted_rows
        mybookapp.people.delete()
        mybookapp.people.insert_many(rows)
        self.client = app.test_client()

    def test_get_all(self):
        response = self.client.get('/api/person/')
        _data = json.loads(response.data)
        assert len(_data) == self.total_rows

    def test_get_limited(self):
        _limit = 3
        _query_string = 'limit=%s' % _limit
        response = self.client.get('/api/person/', query_string=_query_string)
        _data = json.loads(response.data)
        assert len(_data) == _limit + self.info_rows

    def test_get_info_count(self):
        _limit = 3
        _query_string = 'limit=%s' % _limit
        response = self.client.get('/api/person/', query_string=_query_string)
        _data = json.loads(response.data)
        _count = _data[-1:][0]
        assert _count['count'] == self.inserted_rows

class ApiDeleteTestCase(unittest.TestCase):
    
    def setUp(self):
        mybookapp.people.delete()
        self.client = app.test_client()

    def test_delete_without_id(self):
        response = self.client.delete('/api/person/')
        assert response.status_code == 405
        
    def test_delete_person_exists(self):
        _username = 'abnerpc'
        self.client.post(
            '/api/person/',
            data={'facebookId': _username})
        _url = '/api/person/%s' % _username
        response = self.client.delete(_url)
        assert response.status_code == 204

    def test_delete_person_not_exists(self):
        response = self.client.delete('/api/person/35235SFSFS24@$@@$$@$ssff')
        assert response.status_code == 403

    
if __name__ == '__main__':
    unittest.main()
