from unittest import TestCase
from app import app, db
from models import State
from models import StateCases
from tests.runner import clear_db


class TestStateCasesModel(TestCase):

    def setUp(self):
        self.app_context = app.test_request_context()
        self.app_context.push()
        app.test_client()
        self.app = app
        db.create_all()
        self.db = db

    def tearDown(self):
        clear_db(self.db)

    def test_if_save_method_saves_state_case_on_database(self):
        StateCases().save(self.db.session, state_id=1, totalcases=1,
                          totalcasesms=1, notconfirmedbyms=0,
                          deaths=0, url='https://some_url.com.br')
        self.db.session.commit()
        _model = self.db.session.query(StateCases).filter_by(state_id=1).first()
        self.assertIsNotNone(_model)

    def test_if_fetches_all_state_cases_from_database(self):
        State().save(self.db.session, abbreviation='SP', name='São Paulo',
                     lat=12.0001, long=25.0001)
        State().save(self.db.session, abbreviation='SP', name='São Paulo',
                     lat=12.0001, long=25.0001)
        StateCases().save(self.db.session, state_id=1, totalcases=1,
                          totalcasesms=1, notconfirmedbyms=0,
                          deaths=0, url='https://some_url.com.br')
        StateCases().save(self.db.session, state_id=2, totalcases=1,
                          totalcasesms=1, notconfirmedbyms=0,
                          deaths=0, url='https://some_url.com.br')
        self.db.session.commit()
        result = StateCases().fetch_all(self.db.session)
        self.assertEqual(len(result), 2)
