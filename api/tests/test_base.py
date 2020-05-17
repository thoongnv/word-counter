import unittest

from flaskr import create_app
from models.base import db


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('conf.TestingConfig')
        self.client = self.app.test_client()
        # set the databases
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        # drop the databases
        with self.app.app_context():
            db.drop_all()
