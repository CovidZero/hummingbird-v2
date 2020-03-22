import datetime
import json
from unittest import TestCase
from app import app, db
from mock import patch
from models import City
from tests.runner import clear_db


class TestDataApi(TestCase):

    def setUp(self):
        self.app_context = app.test_request_context()
        self.app_context.push()
        self.client = app.test_client()
        self.app = app
        db.create_all()
        self.db = db

    def tearDown(self):
        clear_db(self.db)

    def test_return_cases_by_state_without_reports(self):
        resp = self.client.get('/data_api/v1/data/state/SP')
        data = json.loads(resp.get_data(as_text=True))

        assert len(data) == 4

        assert 'activeCases' in data
        assert 'suspectedCases' in data
        assert 'recoveredCases' in data
        assert 'deaths' in data

        assert data['activeCases'] == 0
        assert data['suspectedCases'] == 0
        assert data['recoveredCases'] == 0
        assert data['deaths'] == 0

    def test_return_cases_by_state_with_reports(self):
        # Generate test data
        City().save(self.db.session, city='Igarapava', state='SP',
                    country='Brasil', total_cases=45, suspects=35, refuses=3, deaths=2, recovered=1)
        City().save(self.db.session, city='Franca', state='SP',
                    country='Brasil', total_cases=50, suspects=35, refuses=3, deaths=1, recovered=1)

        # Should not include this data
        City().save(self.db.session, city='Uberaba', state='MG',
                    country='Brasil', total_cases=50, suspects=35, refuses=3, deaths=1, recovered=1)
        self.db.session.commit()

        resp = self.client.get('/data_api/v1/data/state/SP')
        data = json.loads(resp.get_data(as_text=True))

        assert len(data) == 4

        assert 'activeCases' in data
        assert 'suspectedCases' in data
        assert 'recoveredCases' in data
        assert 'deaths' in data

        assert data['activeCases'] == 14
        assert data['suspectedCases'] == 70
        assert data['recoveredCases'] == 2
        assert data['deaths'] == 3

    def test_return_all_cases(self):
        #generate test data
        City().save(self.db.session, city="c1", state="s1", country="c1", total_cases=20, suspects=5, refuses=3, deaths=2, recovered=1)

        City().save(self.db.session, city="c2", state="s2", country="c1", total_cases=20, suspects=5, refuses=3, deaths=2, recovered=1)

        self.db.session.commit()

        resp = self.client.get('/data_api/v1/data/all')
        data = json.loads(resp.get_data(as_text=True))

        assert len(data) == 4
        
        assert 'activeCases' in data
        assert 'suspectedCases' in data
        assert 'recoveredCases' in data
        assert 'deaths' in data

        assert data['activeCases'] == 18
        assert data['suspectedCases'] == 10
        assert data['recoveredCases'] == 2
        assert data['deaths'] == 4
