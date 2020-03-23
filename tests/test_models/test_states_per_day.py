import datetime
from unittest import TestCase
from app import app, db
from models import StatesPerDay
from tests.runner import clear_db


class TestStatesPerDayMethods(TestCase):

    def setUp(self):
        self.app_context = app.test_request_context()
        self.app_context.push()
        app.test_client()
        self.app = app
        db.create_all()
        self.db = db

    def tearDown(self):
        clear_db(self.db)

    def test_if_save_method_saves_states_per_day_on_database(self):
        StatesPerDay().save(self.db.session, id=1, date=datetime.date.today(),
                            country='Brasil', state='SP', new_cases=35, total_cases=3)
        self.db.session.commit()
        _model = self.db.session.query(StatesPerDay).filter_by(
            state='SP').first()
        self.assertIsNotNone(_model)
