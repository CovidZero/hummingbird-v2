from unittest import TestCase
from app import app, db
from models import CasesLocation
from tests.runner import clear_db


class TestCasesLocationMethods(TestCase):

    def setUp(self):
        self.app_context = app.test_request_context()
        self.app_context.push()
        app.test_client()
        self.app = app
        db.create_all()
        self.db = db

    def tearDown(self):
        clear_db(self.db)

    def test_if_save_method_saves_cases_location_on_database(self):
        CasesLocation().save(self.db.session, id=1, city='c1', state='SP',
                             country='Brasil', status='RECOVERED', latitude=-23.112571, longitude=-50.23952)
        self.db.session.commit()
        _model = self.db.session.query(CasesLocation).filter_by(
            id=1).first()
        self.assertIsNotNone(_model)
