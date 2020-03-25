import json
from unittest import TestCase
from app import app, db
from models import City, CasesLocation
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

    def test_return_cases_by_state_without_reports(self):
        # TODO: Maybe for non existent state we should return
        # TODO: a not found exception with status code 404
        resp = self.client.get(
            '/data_api/v1/data/state/SP',
            headers={
                'Authorization': f"Bearer {self.authentication['access_token']}"
            }
        )
        data = json.loads(resp.get_data(as_text=True))
        self.assertEqual(data, {
            'activeCases': 0,
            'deaths': 0,
            'recoveredCases': 0,
            'suspectedCases': 0
        })

    def test_return_cases_by_state_with_reports(self):
        # Generate test data
        City().save(self.db.session, city='Igarapava', state='SP',
                    country='Brasil', total_cases=45, suspects=35,
                    refuses=3, deaths=2, recovered=1)
        City().save(self.db.session, city='Franca', state='SP',
                    country='Brasil', total_cases=50, suspects=35,
                    refuses=3, deaths=1, recovered=1)
        # Should not include this data
        City().save(self.db.session, city='Uberaba', state='MG',
                    country='Brasil', total_cases=50, suspects=35,
                    refuses=3, deaths=1, recovered=1)
        self.db.session.commit()
        resp = self.client.get(
            '/data_api/v1/data/state/SP',
            headers={
                'Authorization': f"Bearer {self.authentication['access_token']}"
            }
        )
        data = json.loads(resp.get_data(as_text=True))

        self.assertEqual(data, {
            'activeCases': 14,
            'deaths': 3,
            'recoveredCases': 2,
            'suspectedCases': 70
        })

    def test_return_all_cases(self):
        # Seed test data
        City().save(
            self.db.session, city="c1", state="s1",
            country="c1", total_cases=20, suspects=5,
            refuses=3, deaths=2, recovered=1)
        City().save(
            self.db.session, city="c2", state="s2",
            country="c1", total_cases=20, suspects=5,
            refuses=3, deaths=2, recovered=1)
        self.db.session.commit()

        resp = self.client.get(
            '/data_api/v1/data/all',
            headers={
                'Authorization': f"Bearer {self.authentication['access_token']}"
            }
        )
        data = json.loads(resp.get_data(as_text=True))

        self.assertEqual(data, {
            'activeCases': 18,
            'deaths': 4,
            'recoveredCases': 2,
            'suspectedCases': 10
        })

    def test_return_cases_by_search_city(self):
        # Seed test data
        City().save(
            self.db.session, city="c1", state="s1",
            country="c1", total_cases=20, suspects=5,
            refuses=3, deaths=2, recovered=1)
        City().save(
            self.db.session, city="c2", state="s2",
            country="c1", total_cases=20, suspects=5,
            refuses=3, deaths=2, recovered=1)
        self.db.session.commit()

        resp = self.client.get(
            '/data_api/v1/data/search/c1',
            headers={
                'Authorization': f"Bearer {self.authentication['access_token']}"
            }
        )
        data = json.loads(resp.get_data())
        self.assertEqual(len(data), 1)
        self.assertEqual(data, [{
            'city': 'c1',
            'state': 's1',
            'cases': {
                'activeCases': 9,
                'suspectedCases': 5,
                'recoveredCases': 1,
                'deaths': 2
            }
        }])

    def test_return_cases_by_search_state(self):
        # Seed test data
        City().save(
            self.db.session, city="c1", state="s1",
            country="c1", total_cases=20, suspects=5,
            refuses=3, deaths=2, recovered=1)
        City().save(
            self.db.session, city="c2", state="s2",
            country="c1", total_cases=20, suspects=5,
            refuses=3, deaths=2, recovered=1)

        self.db.session.commit()

        resp = self.client.get(
            '/data_api/v1/data/search/s2',
            headers={
                'Authorization': f"Bearer {self.authentication['access_token']}"
            }
        )
        data = json.loads(resp.get_data())
        self.assertEqual(len(data), 1)
        self.assertEqual(data, [{
            'city': 'c2',
            'state': 's2',
            'cases': {
                'activeCases': 9,
                'suspectedCases': 5,
                'recoveredCases': 1,
                'deaths': 2
            }
        }])

    def test_return_cases_by_search_multiple_cities(self):
        # Seed test data
        City().save(self.db.session, city="c1", state="s1",
                    country="c1", total_cases=20, suspects=5,
                    refuses=3, deaths=2, recovered=1)
        City().save(self.db.session, city="c2", state="s2",
                    country="c1", total_cases=20, suspects=5,
                    refuses=3, deaths=2, recovered=1)
        City().save(self.db.session, city="c3", state="s2",
                    country="c1", total_cases=20, suspects=5,
                    refuses=3, deaths=2, recovered=1)
        self.db.session.commit()

        resp = self.client.get(
            '/data_api/v1/data/search/s2',
            headers={
                'Authorization': f"Bearer {self.authentication['access_token']}"
            }
        )
        data = json.loads(resp.get_data())
        self.assertEqual(len(data), 2)
        self.assertEqual(data, [
            {
                'city': 'c2',
                'state': 's2',
                'cases': {
                    'activeCases': 9,
                    'suspectedCases': 5,
                    'recoveredCases': 1,
                    'deaths': 2
                }
            },
            {
                'city': 'c3',
                'state': 's2',
                'cases': {
                    'activeCases': 9,
                    'suspectedCases': 5,
                    'recoveredCases': 1,
                    'deaths': 2
                }
            }
        ])

    # Obter um array de casos de COVID-19 próximos ao usuário
    # /[nome_a_definir]?lat=[LATITUDE]&lng=[LONGITUDE]
    def test_return_cases_near_user(self):
        # Generate test data
        CasesLocation().save(self.db.session, id=0, city='Porto Alegre', state='RS',
                    country='Brasil', status='ACTIVE', latitude=-29.974343, longitude=-51.195532)
        CasesLocation().save(self.db.session, id=1, city='Porto Alegre', state='RS',
                    country='Brasil', status='SUSPECTED', latitude=-29.974343, longitude=-51.195532)
        CasesLocation().save(self.db.session, id=2, city='Porto Alegre', state='RS',
                    country='Brasil', status='RECOVERED', latitude=-29.974343, longitude=-51.195532)

        # Should not include this data
        CasesLocation().save(self.db.session, id=3, city='Igarapava', state='SP',
                    country='Brasil', status='RECOVERED', latitude=-20.047582, longitude=-47.780110)
        self.db.session.commit()

        resp = self.client.get(
            '/data_api/v1/data/cases_location?lat=-29.974343&lng=-51.195532',
            headers={
                'Authorization': f"Bearer {self.authentication['access_token']}"
            }
        )
        data = json.loads(resp.get_data(as_text=True))
        self.assertEqual(data['status'], 'ACTIVE')



