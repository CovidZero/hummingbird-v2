import datetime
from app import app, db
from unittest import TestCase
from models import State
from models import StateCases
from models import StateCasesPerDay
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
        State().save(self.db.session, abbreviation='SP', name='São Paulo',
                     lat= 12.0001, lng= 25.0001)
        State().save(self.db.session, abbreviation='SP', name='São Paulo',
                     lat= 12.0001, lng= 25.0001)
        StateCases().save(self.db.session, state_id=1, totalcases=1,
                          totalcasesms=1, notconfirmedbyms=0,
                          deaths=0, url='https://some_url.com.br')
        StateCases().save(self.db.session, state_id=2, totalcases=1,
                          totalcasesms=1, notconfirmedbyms=0,
                          deaths=0, url='https://some_url.com.br')
        self.db.session.commit()
        result = state_services.get_state_cases()
        self.assertEqual(len(result), 2)
        self.assertEqual(result, [{
            "stateCode": "SP",
            "stateName": "São Paulo",
            "lat": 12.0001,
            "lng": 25.0001,
            "cases": {
                "totalCases": 1,
                "deaths": 0
            }
        }, {
            "stateCode": "SP",
            "stateName": "São Paulo",
            "lat": 12.0001,
            "lng": 25.0001,
            "cases": {
                "totalCases": 1,
                "deaths": 0
            }
        }])

    def test_if_returns_when_state_cases_not_exists(self):
        result = state_services.get_state_cases()

        self.assertEqual(len(result), 0)
        self.assertEqual(result, [])

    def test_if_returns_a_daily_state_list_with_pagination(self):
        State().save(self.db.session, abbreviation='SP',
                     name='São Paulo',
                     lat=12.0001, lng=25.0001)
        StateCasesPerDay().save(self.db.session, id=1, date=datetime.date(2020, 3, 29),
                                country='Brazil', state_id=1, newcases=3, totalcases=35)
        StateCasesPerDay().save(self.db.session, id=2, date=datetime.date(2020, 3, 30),
                                country='Brazil', state_id=1, newcases=3, totalcases=38)
        self.db.session.commit()
        result = state_services.get_daily_state_cases(1)
        self.assertEqual(result, {
            'cases': [
                {
                    "stateCode": "SP",
                    "stateName": "São Paulo",
                    "lat": 12.0001,
                    "lng": 25.0001,
                    "country": "Brazil",
                    "date": "2020-03-29",
                    "case_detail": {
                        "newCases": 3,
                        "totalCases": 35
                    }
                },
                {
                    "stateCode": "SP",
                    "stateName": "São Paulo",
                    "lat": 12.0001,
                    "lng": 25.0001,
                    "country": "Brazil",
                    "date": "2020-03-30",
                    "case_detail": {
                        "newCases": 3,
                        "totalCases": 38
                    }
                }
            ],
            'pagination': {
                'total_pages': 1,
                'has_next': False,
                'has_previous': False,
                'next_page': None,
                'current_page': 1,
            }
        })
