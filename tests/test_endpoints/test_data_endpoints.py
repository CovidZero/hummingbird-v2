import json
from unittest import TestCase
from app import app, db
from models import State
from models import StateCases
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

    def test_return_all_state_cases_cases(self):
        State().save(self.db.session, state='SP', country='Brasil',
                     lat='12.0000', lng='25.0000')
        State().save(self.db.session, state='SP', country='Brasil',
                     lat='12.0000', lng='25.0000')
        StateCases().save(self.db.session, state=1, totalcases=1,
                          totalcasesms=1, notconfirmedbyms=0,
                          deaths=0, url='https://some_url.com.br')
        StateCases().save(self.db.session, state=2, totalcases=1,
                          totalcasesms=1, notconfirmedbyms=0,
                          deaths=0, url='https://some_url.com.br')
        self.db.session.commit()

        resp = self.client.get(
            '/data_api/v1/data/state/cases/all',
            headers={
                'Authorization': f"Bearer {self.authentication['access_token']}"
            }
        )
        response = json.loads(resp.get_data(as_text=True))
        self.assertEqual(len(response), 2)
        self.assertEqual(response, [{
            "stateCode": "SP",
            "lat": "12.0000",
            "lng": "25.0000",
            "cases": {
                "activeCases": 1,
                "deaths": 0
            }
        }, {
            "stateCode": "SP",
            "lat": "12.0000",
            "lng": "25.0000",
            "cases": {
                "activeCases": 1,
                "deaths": 0
            }
        }])




