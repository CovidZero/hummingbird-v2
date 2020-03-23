from unittest import TestCase
from app import app, db
from models import City
from tests.runner import clear_db


class TestCityMethods(TestCase):

    def setUp(self):
        self.app_context = app.test_request_context()
        self.app_context.push()
        app.test_client()
        self.app = app
        db.create_all()
        self.db = db

    def tearDown(self):
        clear_db(self.db)

    def test_if_save_method_saves_city_on_database(self):
        City().save(self.db.session, city='city1', state='SP',
                    country='Brasil', total_cases=45, suspects=35, refuses=3, deaths=2, recovered=1)
        self.db.session.commit()
        _model = self.db.session.query(City).filter_by(city='city1').first()
        self.assertIsNotNone(_model)

    def test_city_active_cases(self):
        new_city = City().save(self.db.session, city='city1', state='SP',
                               country='Brasil', total_cases=45, suspects=35, refuses=3, deaths=2, recovered=1)
        assert new_city.active_cases == 4
