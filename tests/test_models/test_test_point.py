from unittest import TestCase
from app import app, db
from models import TestPoint
from tests.runner import clear_db


class TestTestPointMethods(TestCase):

    def setUp(self):
        self.app_context = app.test_request_context()
        self.app_context.push()
        app.test_client()
        self.app = app
        db.create_all()
        self.db = db

    def tearDown(self):
        clear_db(self.db)

    def test_if_save_method_saves_test_point_on_database(self):
        TestPoint().save(self.db.session, id=1, name='hospital1',
                         address='some address', city='c1', zip_code='13547895',
                         latitude=-23.112571, longitude=-50.23952)
        self.db.session.commit()
        _model = self.db.session.query(TestPoint).filter_by(
            name='hospital1').first()
        self.assertIsNotNone(_model)
