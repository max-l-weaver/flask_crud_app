#!/user/bin/python
import os
import unittest
import os
import unittest
import tempfile
import crudapp
# from flask_testing import TestCase

class User():

    def __init__(self, id, username, ip, timestamp):
        self.id = id
        self.username = username
        self.ip = ip
        self.timestmap = timestamp


class crudAppTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, crudapp.app.config['DATABASE'] = tempfile.mkstemp()
        crudapp.app.config['TESTING'] = True
        self.app = crudapp.app.test_client()
        with crudapp.app.app_context():
            crudapp.db.create_all()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(crudapp.app.config['DATABASE'])

    def test_homepage(self):
        rv = self.app.get('/')
        assert b"Welcome to the world's greatest CRUD app" in rv.data

    def create_new_user(self):
        rv = self.app.post('/user/',
                            data=json.dumps(dict(username='max')),
                            content_type="application/json")


if __name__ == '__main__':
    unittest.main()
