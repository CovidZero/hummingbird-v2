from app import app, db
from unittest import TestCase
from models import DataSus
from apis.data import datasus_services
from tests.runner import clear_db
import datetime

class TestDataSusServices(TestCase):
    def setUp(self):
        self.app_context = app.test_request_context()
        self.app_context.push()
        self.client = app.test_client()
        self.app = app
        db.create_all()
        self.db = db

    def tearDown(self):
        clear_db(self.db)

    def test_sus_list_return_all_cases_without_pagination(self):
        DataSus().save(self.db.session, id=1, region='region', state='state', date=datetime.date(2020, 3, 29),
                       newcases=1, totalcases=2, newdeaths=1, totaldeaths=1, update=datetime.date(2020, 3, 29))

        DataSus().save(self.db.session, id=2, region='region2', state='state2', date=datetime.date(2020, 3, 29),
                       newcases=1, totalcases=2, newdeaths=1, totaldeaths=1, update=datetime.date(2020, 3, 29))

        self.db.session.commit()

        response = datasus_services.get_sus_list(None)

        self.assertEqual(len(response.get('sus_list')), 2)


    def test_sus_list_return_all_cases_paginated(self):
        DataSus().save(self.db.session, id=1, region='region', state='state', date=datetime.date(2020, 3, 29),
                       newcases=1, totalcases=2, newdeaths=1, totaldeaths=1, update=datetime.date(2020, 3, 29))

        DataSus().save(self.db.session, id=2, region='region2', state='state2', date=datetime.date(2020, 3, 29),
                       newcases=1, totalcases=2, newdeaths=1, totaldeaths=1, update=datetime.date(2020, 3, 29))

        self.db.session.commit()

        response = datasus_services.get_sus_list(1)

        self.assertEqual(len(response.get('sus_list')), 2)
