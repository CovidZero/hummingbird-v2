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

    def test_sus_graphs_last_30_days(self):
        # Return only the last 30 elements
        for days_amount in range(31):
            current_day = datetime.date.today() - datetime.timedelta(days=days_amount)
            DataSus().save(self.db.session, id=days_amount, region='Brasil', state='state', date=current_day,
                           newcases=1, totalcases=2, newdeaths=1, totaldeaths=1, update=current_day)

        self.db.session.commit()

        response = datasus_services.get_graph_last_30_days()

        self.assertEqual(len(response), 30)
        for current_date in response:
            self.assertIn('date', current_date.keys())
            self.assertIn('totalCases', current_date.keys())
            self.assertIn('totalDeaths', current_date.keys())

    def test_sus_graphs_total_cases(self):
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        DataSus().save(self.db.session, id=1, region='region_1', state='state',
                       city='city', coduf=1, codmun=2, population=100000,
                       date=datetime.date.today(),
                       newcases=1, totalcases=2, newdeaths=1, totaldeaths=1,
                       update=datetime.date.today())
        DataSus().save(self.db.session, id=2, region='region_2', state='state',
                       city='city', coduf=1, codmun=2, population=100000,
                       date=yesterday,
                       newcases=1, totalcases=2, newdeaths=1, totaldeaths=1,
                       update=yesterday)
        DataSus().save(self.db.session, id=3, region='region_2', state='state',
                       city='city', coduf=76, codmun=2, population=100000,
                       date=datetime.date.today(),
                       newcases=1, totalcases=2, newdeaths=1, totaldeaths=1,
                       update=datetime.date.today())

        self.db.session.commit()

        response = datasus_services.get_graph_total_cases()

        self.assertEqual(len(response), 1)
        for current_date in response:
            self.assertIn('region', current_date.keys())
            self.assertIn('date', current_date.keys())
            self.assertIn('totalCases', current_date.keys())
            self.assertIn('totalDeaths', current_date.keys())

    def test_sus_regions(self):
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        DataSus().save(self.db.session, id=1, region='region_1', state='state',
                       city='city', coduf=1, codmun=2, population=100000,
                       date=datetime.date.today(),
                       newcases=1, totalcases=2, newdeaths=1, totaldeaths=1,
                       update=datetime.date.today())
        DataSus().save(self.db.session, id=2, region='region_2', state='state',
                       city='city', coduf=1, codmun=2, population=100000,
                       date=yesterday,
                       newcases=1, totalcases=2, newdeaths=1, totaldeaths=1,
                       update=yesterday)
        DataSus().save(self.db.session, id=3, region='region_2', state='state',
                       city='city', coduf=1, codmun=2, population=100000,
                       date=datetime.date.today(),
                       newcases=1, totalcases=2, newdeaths=1, totaldeaths=1,
                       update=datetime.date.today())

        self.db.session.commit()

        response = datasus_services.get_regions()

        self.assertEqual(len(response), 2)
        for current_date in response:
            self.assertIn('id', current_date.keys())
            self.assertIn('region', current_date.keys())
            self.assertIn('state', current_date.keys())
            self.assertIn('city', current_date.keys())
            self.assertIn('coduf', current_date.keys())
            self.assertIn('codmun', current_date.keys())
            self.assertIn('population', current_date.keys())
            self.assertIn('date', current_date.keys())
            self.assertIn('totalCases', current_date.keys())
            self.assertIn('totalDeaths', current_date.keys())
