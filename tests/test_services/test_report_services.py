from app import app, db
from unittest import TestCase
from models import City, State
from apis.data.services import ReportService
from tests.runner import clear_db


class TestReportService(TestCase):
    def setUp(self):
        self.app_context = app.test_request_context()
        self.app_context.push()
        self.client = app.test_client()
        self.app = app
        db.create_all()
        self.db = db

    def tearDown(self):
        clear_db(self.db)

    def test_search_on_location_by_term_returns_data_when_exists(self):
        State().save(self.db.session, id=1, name="state1", abbreviation="s1", lat=0, lng=0)
        City().save(self.db.session, id=1, city='c1', ibge_id=1,
                    country='Country1', state_id=1, totalcases=10)
        City().save(self.db.session, id=2, city='c2', ibge_id=2,
                    country='Country1', state_id=1, totalcases=20)
        self.db.session.commit()

        response = ReportService().search_on_location_by_term('c1')

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

        response = ReportService().search_on_location_by_term('c3')

        self.assertEqual(len(response), 0)
        self.assertEqual(response, [])