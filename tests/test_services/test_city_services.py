from app import app, db
from unittest import TestCase

from models import City, State
from apis.data import city_services
from tests.runner import clear_db


class TestCityServices(TestCase):

    def setUp(self):
        self.app_context = app.test_request_context()
        self.app_context.push()
        self.client = app.test_client()
        self.app = app
        db.create_all()
        self.db = db

    def tearDown(self):
        clear_db(self.db)

    def test_city_cases_return_all_cases_without_pagination(self):
        City().save(self.db.session, id=1, city='c1', ibge_id=1,
                    country='Country1', state_id=1, totalcases=10)
        City().save(self.db.session, id=2, city='c2', ibge_id=2,
                    country='Country1', state_id=1, totalcases=20)
        self.db.session.commit()

        response = city_services.get_city_cases(None)

        self.assertEqual(len(response.get('cases')), 2)
        self.assertEqual(response, {
            'cases': [{
                'city': 'c1',
                'ibge_id': 1,
                'country': 'Country1',
                'state_id': 1,
                'totalcases': 10
            }, {
                'city': 'c2',
                'ibge_id': 2,
                'country': 'Country1',
                'state_id': 1,
                'totalcases': 20
            }],
            'pagination': {}})

    def test_search_on_location_by_term_returns_data_when_exists(self):
        State().save(self.db.session, id=1, name="state1", abbreviation="s1", lat=0, lng=0)
        City().save(self.db.session, id=1, city='c1', ibge_id=1,
                    country='Country1', state_id=1, totalcases=10)
        City().save(self.db.session, id=2, city='c2', ibge_id=2,
                    country='Country1', state_id=1, totalcases=20)
        self.db.session.commit()

        response = city_services.search_on_location_by_term('c1')

        self.assertEqual(len(response), 1)
        self.assertEqual(response, [{'city': 'c1',
                                     'state': 'state1',
                                     'cases': {
                                         'totalCases': 10
                                     }}])

    def test_search_on_location_by_term_returns_Null_when_not_exists(self):
        State().save(self.db.session, id=1, name="state1", abbreviation="s1", lat=0, lng=0)
        City().save(self.db.session, id=1, city='c1', ibge_id=1,
                    country='Country1', state_id=1, totalcases=10)
        City().save(self.db.session, id=2, city='c2', ibge_id=2,
                    country='Country1', state_id=1, totalcases=20)
        self.db.session.commit()

        response = city_services.search_on_location_by_term('c3')

        self.assertEqual(len(response), 0)
        self.assertEqual(response, [])

    def test_city_cases_return_cases_with_pagination(self):
        City().save(self.db.session, id=1, city='c1', ibge_id=1,
                    country='Country1', state_id=1, totalcases=10)
        City().save(self.db.session, id=2, city='c2', ibge_id=2,
                    country='Country1', state_id=1, totalcases=20)
        self.db.session.commit()

        response = city_services.get_city_cases(1)

        self.assertEqual(len(response.get('cases')), 2)
        self.assertEqual(response, {
            'cases': [{
                'city': 'c1',
                'ibge_id': 1,
                'country': 'Country1',
                'state_id': 1,
                'totalcases': 10
            }, {
                'city': 'c2',
                'ibge_id': 2,
                'country': 'Country1',
                'state_id': 1,
                'totalcases': 20
            }],
            'pagination': {'current_page': 1,
                           'has_next': False,
                           'has_previous': False,
                           'next_page': None,
                           'total_pages': 1}})

    def test_city_cases_return_cases_without_restrained_cities(self):
        City().save(self.db.session, id=1, city='NÃO ESPECIFICADA', ibge_id=1,
                    country='Country1', state_id=1, totalcases=10)
        City().save(self.db.session, id=2, city='FORA DO ESTADO', ibge_id=2,
                    country='Country1', state_id=1, totalcases=10)

        City().save(self.db.session, id=3, city='ESTRANGEIRO', ibge_id=3,
                    country='Country1', state_id=1, totalcases=10)

        City().save(self.db.session, id=4, city='c1', ibge_id=4,
                    country='Country1', state_id=1, totalcases=20)
        self.db.session.commit()

        response = city_services.get_city_cases(None)

        self.assertEqual(len(response.get('cases')), 1)
        self.assertEqual(response, {
            'cases': [{
                'city': 'c1',
                'ibge_id': 4,
                'country': 'Country1',
                'state_id': 1,
                'totalcases': 20
            }],
            'pagination': {}})

    def test_city_cases_paginated_return_cases_without_restrained_cities(self):
        City().save(self.db.session, id=1, city='NÃO ESPECIFICADA', ibge_id=1,
                    country='Country1', state_id=1, totalcases=10)
        City().save(self.db.session, id=2, city='FORA DO ESTADO', ibge_id=2,
                    country='Country1', state_id=1, totalcases=10)

        City().save(self.db.session, id=3, city='ESTRANGEIRO', ibge_id=3,
                    country='Country1', state_id=1, totalcases=10)

        City().save(self.db.session, id=4, city='c1', ibge_id=4,
                    country='Country1', state_id=1, totalcases=20)
        self.db.session.commit()

        response = city_services.get_city_cases(1)

        self.assertEqual(len(response.get('cases')), 1)
        self.assertEqual(response, {
            'cases': [{
                'city': 'c1',
                'ibge_id': 4,
                'country': 'Country1',
                'state_id': 1,
                'totalcases': 20
            }],
            'pagination': {'current_page': 1,
                           'has_next': False,
                           'has_previous': False,
                           'next_page': None,
                           'total_pages': 1}})


    def test_search_on_location_by_term_return_cases_without_restrained_cities(self):
        State().save(self.db.session, id=1, name="state1", abbreviation="s1", lat=0, lng=0)
        City().save(self.db.session, id=1, city='NÃO ESPECIFICADA', ibge_id=1,
                    country='Country1', state_id=1, totalcases=10)
        City().save(self.db.session, id=2, city='FORA DO ESTADO', ibge_id=2,
                    country='Country1', state_id=1, totalcases=10)

        City().save(self.db.session, id=3, city='ESTRANGEIRO', ibge_id=3,
                    country='Country1', state_id=1, totalcases=10)

        City().save(self.db.session, id=4, city='c1', ibge_id=4,
                    country='Country1', state_id=1, totalcases=20)
        self.db.session.commit()

        response = city_services.search_on_location_by_term('c1')

        self.assertEqual(len(response), 1)
        self.assertEqual(response, [{
            'city': 'c1',
            'state': 'state1',
            'cases': {
                'totalCases': 20
            }
        }])

    def test_get_totals_cases_per_city_ignore_restrained_cities(self):
        City().save(self.db.session, id=1, city='NÃO ESPECIFICADA', ibge_id=1,
                    country='Country1', state_id=1, totalcases=10)
        City().save(self.db.session, id=2, city='FORA DO ESTADO', ibge_id=2,
                    country='Country1', state_id=1, totalcases=10)

        City().save(self.db.session, id=3, city='ESTRANGEIRO', ibge_id=3,
                    country='Country1', state_id=1, totalcases=10)

        City().save(self.db.session, id=4, city='c1', ibge_id=4,
                    country='Country1', state_id=1, totalcases=20)
        self.db.session.commit()

        response = city_services.get_totals_cases_per_city()

        self.assertEqual(response, {'totalCases': 50})
