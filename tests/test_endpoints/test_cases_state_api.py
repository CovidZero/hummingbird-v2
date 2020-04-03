import json
import datetime
from unittest import TestCase
from app import app, db
from models import State, StateCases, StateCasesPerDay
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

    def test_endpoint_list_state_cases_daily(self):
        # Seed test data
        State().save(self.db.session, abbreviation='SP',
                     name='São Paulo',
                     lat=12.0001, lng=25.0001)
        StateCasesPerDay().save(self.db.session, id=1, date=datetime.date(2020, 3, 29),
                                country='Brazil', state_id=1, newcases=3, totalcases=35)
        self.db.session.commit()
        resp = self.client.get(
            '/data_api/v1/cases/state/daily/1',
            headers={
                'Authorization': f"Bearer {self.authentication['access_token']}"
            }
        )
        result = json.loads(resp.get_data(as_text=True))
        self.assertEqual(result, {"cases": [{
                 "stateCode": "SP",
                 "stateName": "São Paulo",
                 "lat": "12.0001",
                 "lng": "25.0001",
                 "country": "Brazil",
                 "date": "2020-03-29",
                 "case_detail": {
                     "totalCases": 35,
                     "newCases": 3
                 }}
            ],
            "pagination": {
                "total_pages": 1,
                "has_next": False,
                "has_previous": False,
                "next_page": None,
                "current_page": 1
            }
        })


