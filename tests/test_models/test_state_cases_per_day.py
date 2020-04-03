import datetime
from unittest import TestCase
from app import app, db
from tests.runner import clear_db
from models import State
from models import StateCasesPerDay


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
        StateCasesPerDay().save(self.db.session, id=1, date=datetime.date.today(),
                                country='Brasil', state_id=1, newcases=35, totalcases=3)
        self.db.session.commit()
        _model = self.db.session.query(StateCasesPerDay).filter_by(
            state_id=1).first()
        self.assertIsNotNone(_model)

    def test_if_fetches_all_cases_per_day(self):
        State().save(self.db.session, abbreviation='SP',
                     name='São Paulo',
                     lat=12.0001, lng=25.0001)
        StateCasesPerDay().save(self.db.session, id=1, date=datetime.date(2020, 3, 29),
                                country='Brasil', state_id=1, newcases=35, totalcases=3)
        StateCasesPerDay().save(self.db.session, id=2, date=datetime.date(2020, 3, 30),
                                country='Brasil', state_id=1, newcases=35, totalcases=3)
        StateCasesPerDay().save(self.db.session, id=3, date=datetime.date(2020, 4, 1),
                                country='Brasil', state_id=1, newcases=35, totalcases=3)
        StateCasesPerDay().save(self.db.session, id=4, date=datetime.date(2020, 4, 2),
                                country='Brasil', state_id=1, newcases=35, totalcases=3)
        self.db.session.commit()
        cases_list = StateCasesPerDay().fetch_all(self.db.session)
        self.assertEqual(len(cases_list), 4)

    def test_if_fetches_all_cases_per_day_paginated(self):
        State().save(self.db.session, abbreviation='SP',
                     name='São Paulo',
                     lat=12.0001, lng=25.0001)
        StateCasesPerDay().save(self.db.session, id=1, date=datetime.date(2020, 3, 29),
                                country='Brasil', state_id=1, newcases=35, totalcases=3)
        StateCasesPerDay().save(self.db.session, id=2, date=datetime.date(2020, 3, 30),
                                country='Brasil', state_id=1, newcases=35, totalcases=3)
        StateCasesPerDay().save(self.db.session, id=3, date=datetime.date(2020, 4, 1),
                                country='Brasil', state_id=1, newcases=35, totalcases=3)
        StateCasesPerDay().save(self.db.session, id=4, date=datetime.date(2020, 4, 2),
                                country='Brasil', state_id=1, newcases=35, totalcases=3)
        self.db.session.commit()
        cases_list, pagination = StateCasesPerDay().fetch_paginated(self.db.session, 1)
        self.assertEqual(len(cases_list), 4)
        self.assertEqual(pagination, {
            'total_pages': 1,
            'has_next': False,
            'has_previous': False,
            'next_page': None,
            'current_page': 1,
        })


