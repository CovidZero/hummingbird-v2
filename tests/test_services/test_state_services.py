from app import app, db
from unittest import TestCase
from models import State
from models import StateCases
from apis.data import state_services
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

    def test_if_returns_all_state_cases_from_database(self):
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
        result = state_services.get_all_state_cases()
        self.assertEqual(len(result), 2)
        self.assertEqual(result, [{
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
