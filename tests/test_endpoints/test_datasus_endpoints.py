import json
import datetime
from unittest import TestCase
from app import app, db
from models import DataSus
from tests.runner import clear_db


class TestDataSusEndpoints(TestCase):

    def setUp(self):
        self.app_context = app.test_request_context()
        self.app_context.push()
        self.client = app.test_client()
        self.app = app
        db.create_all()
        self.db = db

    def tearDown(self):
        clear_db(self.db)

    def test_return_all_sus_list(self):
        DataSus().save(self.db.session, id=1, region='region', state='state', date=datetime.date(2020, 3, 29),
                       newcases=1, totalcases=2, newdeaths=1, totaldeaths=1, update=datetime.date(2020, 3, 29))

        DataSus().save(self.db.session, id=2, region='region2', state='state2', date=datetime.date(2020, 3, 29),
                       newcases=1, totalcases=2, newdeaths=1, totaldeaths=1, update=datetime.date(2020, 3, 29))

        self.db.session.commit()


        resp = self.client.get('/data_api/v1/cases/datasus')
        response = json.loads(resp.get_data(as_text=True))

        self.assertEqual(len(response.get('sus_list')), 2)
        self.assertEqual(resp.status_code, 200)

    def test_return_404_when_sus_list_empty(self):
        resp = self.client.get('/data_api/v1/cases/datasus')

        self.assertEqual(resp.status_code, 404)

    def test_return_sus_list_paginated(self):
        DataSus().save(self.db.session, id=1, region='region', state='state', date=datetime.date(2020, 3, 29),
                       newcases=1, totalcases=2, newdeaths=1, totaldeaths=1, update=datetime.date(2020, 3, 29))

        DataSus().save(self.db.session, id=2, region='region2', state='state2', date=datetime.date(2020, 3, 29),
                       newcases=1, totalcases=2, newdeaths=1, totaldeaths=1, update=datetime.date(2020, 3, 29))

        self.db.session.commit()

        resp = self.client.get('/data_api/v1/cases/datasus/1')
        response = json.loads(resp.get_data(as_text=True))

        self.assertEqual(len(response.get('sus_list')), 2)
        self.assertEqual(resp.status_code, 200)


    def test_sus_list_paginated_return_404_when_page_not_exists(self):
        resp = self.client.get('/data_api/v1/cases/datasus/2')

        self.assertEqual(resp.status_code, 404)

