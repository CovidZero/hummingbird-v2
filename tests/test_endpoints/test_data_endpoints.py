import json
from unittest import TestCase
from app import app, db
from models import State
from models import StateCases
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

        # Endpoints Authentication Setup
        response = self.client.post(
            f"/data_api/v1/authorization/create_tokens",
            json={"username": self.app.config['AUTH_USERNAME'],
                  "password": self.app.config['AUTH_PASSWORD']}
        )
        self.authentication = json.loads(response.data)

    def tearDown(self):
        clear_db(self.db)

    def test_return_all_cases_per_state(self):
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
            '/data_api/v1/cases/state',
            headers={
                'Authorization': f"Bearer {self.authentication['access_token']}"
            }
        )
        response = json.loads(resp.get_data(as_text=True))
        self.assertEqual(len(response), 2)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(response, [{
            "stateCode": "SP",
            "stateName": "São Paulo",
            "lat": "12.0001",
            "lng": "25.0001",
            "cases": {
                "totalCases": 1,
                "deaths": 0
            }
        }, {
            "stateCode": "MG",
            "stateName": "Minas Gerais",
            "lat": "13.0001",
            "lng": "26.0001",
            "cases": {
                "totalCases": 5,
                "deaths": 8
            }
        }])

    def test_cases_per_state_return_404_when_empty_data(self):
        resp = self.client.get(
            '/data_api/v1/cases/state',
            headers={
                'Authorization': f"Bearer {self.authentication['access_token']}"
            }
        )

        self.assertEqual(resp.status_code, 404)


    def test_state_report_return_404_when_empty_data(self):
        resp = self.client.get(
            '/data_api/v1/cases/state/report',
            headers={
                'Authorization': f"Bearer {self.authentication['access_token']}"
            }
        )

        self.assertEqual(resp.status_code, 404)


    def test_state_report_return_all_data(self):
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
        response = json.loads(resp.get_data(as_text=True))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(response, {
            "totalCases": '6',
            "totalCasesMS": '4',
            "deaths": '8'
        })

    def test_return_all_city_cases(self):
        City().save(self.db.session, id=1, city='c1', ibge_id=1,
                    country='Country1', state_id=1, totalcases=10)
        City().save(self.db.session, id=2, city='c2', ibge_id=2,
                    country='Country1', state_id=1, totalcases=20)
        self.db.session.commit()

        resp = self.client.get(
            '/data_api/v1/cases/city',
            headers={
                'Authorization': f"Bearer {self.authentication['access_token']}"
            }
        )

        response = json.loads(resp.get_data(as_text=True))

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(response, {
            'cases': [{
                'id': None,
                'city': 'c1',
                'ibge_id': '1',
                'country': 'Country1',
                'state_id': 1,
                'totalcases': 10
            }, {
                'id': None,
                'city': 'c2',
                'ibge_id': '2',
                'country': 'Country1',
                'state_id': 1,
                'totalcases': 20
            }]
        })

    def test_return_404_when_city_cases_empty(self):
        resp = self.client.get(
            '/data_api/v1/cases/city',
            headers={
                'Authorization': f"Bearer {self.authentication['access_token']}"
            }
        )

        self.assertEqual(resp.status_code, 404)

    def test_return_all_city_cases_paginated(self):
        City().save(self.db.session, id=1, city='c1', ibge_id=1,
                    country='Country1', state_id=1, totalcases=10)
        City().save(self.db.session, id=2, city='c2', ibge_id=2,
                    country='Country1', state_id=1, totalcases=20)
        self.db.session.commit()

        resp = self.client.get(
            '/data_api/v1/cases/city/1',
            headers={
                'Authorization': f"Bearer {self.authentication['access_token']}"
            }
        )
        response = json.loads(resp.get_data(as_text=True))

        self.assertEqual(resp.status_code, 200)
        self.maxDiff = None
        self.assertEqual(response, {
            'cases': [{
                'id': None,
                'city': 'c1',
                'ibge_id': '1',
                'country': 'Country1',
                'state_id': 1,
                'totalcases': 10
            }, {
                'id': None,
                'city': 'c2',
                'ibge_id': '2',
                'country': 'Country1',
                'state_id': 1,
                'totalcases': 20
            }],
            'pagination': {'current_page': 1,
                           'has_next': False,
                           'has_previous': False,
                           'next_page': None,
                           'total_pages': 1}

        })

    def test_city_cases_return_404_when_page_not_exists(self):
        City().save(self.db.session, id=1, city='c1', ibge_id=1,
                    country='Country1', state_id=1, totalcases=10)
        self.db.session.commit()

        resp = self.client.get(
            '/data_api/v1/cases/city/2',
            headers={
                'Authorization': f"Bearer {self.authentication['access_token']}"
            }
        )

        self.assertEqual(resp.status_code, 404)

    def test_return_all_city_reports(self):
        City().save(self.db.session, id=1, city='c1', ibge_id=1,
                    country='Country1', state_id=1, totalcases=10)
        City().save(self.db.session, id=2, city='c2', ibge_id=2,
                    country='Country1', state_id=1, totalcases=20)
        self.db.session.commit()

        resp = self.client.get(
            '/data_api/v1/cases/city/report',
            headers={
                'Authorization': f"Bearer {self.authentication['access_token']}"
            }
        )
        response = json.loads(resp.get_data(as_text=True))

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(response, {'totalCases': 30})

    def test_city_report_return_404_when_data_is_empty(self):
        resp = self.client.get(
            '/data_api/v1/cases/city/report',
            headers={
                'Authorization': f"Bearer {self.authentication['access_token']}"
            }
        )

        self.assertEqual(resp.status_code, 404)

    def test_return_city_report_by_term_when_data_exists(self):
        State().save(self.db.session, id=1, name="state1", abbreviation="s1", lat=0, lng=0)
        City().save(self.db.session, id=1, city='c1', ibge_id=1,
                    country='Country1', state_id=1, totalcases=10)
        City().save(self.db.session, id=2, city='c2', ibge_id=2,
                    country='Country1', state_id=1, totalcases=20)
        self.db.session.commit()

        resp = self.client.get(
            '/data_api/v1/cases/city/c1/report',
            headers={
                'Authorization': f"Bearer {self.authentication['access_token']}"
            }
        )
        response = json.loads(resp.get_data(as_text=True))

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(response, [{'city': 'c1', 'state': 'state1', 'cases': {'totalCases': 10}}])

    def test_return_404_when_city_report_by_term_not_exists(self):
        State().save(self.db.session, id=1, name="state1", abbreviation="s1", lat=0, lng=0)
        City().save(self.db.session, id=1, city='c1', ibge_id=1,
                    country='Country1', state_id=1, totalcases=10)
        City().save(self.db.session, id=2, city='c2', ibge_id=2,
                    country='Country1', state_id=1, totalcases=20)
        self.db.session.commit()

        resp = self.client.get(
            '/data_api/v1/cases/city/c3/report',
            headers={
                'Authorization': f"Bearer {self.authentication['access_token']}"
            }
        )

        self.assertEqual(resp.status_code, 404)
