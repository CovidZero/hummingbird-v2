import json
from unittest import TestCase
from app import app, db
from models import City, CasesLocation, State, StateCases
from tests.runner import clear_db


class TestDataApi(TestCase):

    def setUp(self):
        self.app_context = app.test_request_context()
        self.app_context.push()
        self.client = app.test_client()
        self.app = app
        db.create_all()
        self.db = db

        # Endpoints Authentication Setup
        response = self.client.post(
            f"/data_api/v1/authorization/create_tokens",
            json={"username": self.app.config['AUTH_USERNAME'],
                  "password": self.app.config['AUTH_PASSWORD']}
        )
        self.authentication = json.loads(response.data)

    def tearDown(self):
        clear_db(self.db)

    def test_return_all_cases(self):
        # Seed test data
        State().save(self.db.session, abbreviation='SP', name='São Paulo',
                     lat=12.0001, lng=25.0001)
        State().save(self.db.session, abbreviation='MG', name='Minas Gerais',
                     lat=13.0001, lng=26.0001)
        StateCases().save(self.db.session, state_id=1, totalcases=1,
                          totalcasesms=1, notconfirmedbyms=0,
                          deaths=0, url='https://some_url.com.br')
        StateCases().save(self.db.session, state_id=2, totalcases=5,
                          totalcasesms=3, notconfirmedbyms=2,
                          deaths=8, url='https://some_url.com.br')
        self.db.session.commit()
        resp = self.client.get(
            '/data_api/v1/cases/state/report',
            headers={
                'Authorization': f"Bearer {self.authentication['access_token']}"
            }
        )
        data = json.loads(resp.get_data(as_text=True))

        self.assertEqual(data, {
            'totalCases': '6',
            'totalCasesMS': '4',
            'deaths': '8'
        })

    def test_return_cases_by_search_city(self):
        # Seed test data
        State().save(self.db.session, abbreviation='SP', name='São Paulo',
                     lat=12.0001, lng=25.0001)
        City().save(
            self.db.session, id=1, city="c1", state_id=1,
            country="c1", totalcases=20)
        City().save(
            self.db.session, id=2, city="c2", state_id=2,
            country="c1", totalcases=20)
        self.db.session.commit()

        resp = self.client.get(
            '/data_api/v1/cases/city/c1/report',
            headers={
                'Authorization': f"Bearer {self.authentication['access_token']}"
            }
        )
        data = json.loads(resp.get_data())
        self.assertEqual(len(data), 1)
        self.assertEqual(data, [{
            'city': 'c1',
            'state': 'São Paulo',
            'cases': {
                'totalCases': 20,
            }
        }])
