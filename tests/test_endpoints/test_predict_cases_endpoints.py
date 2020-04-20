import json
import datetime
from unittest import TestCase
from app import app, db
from models import PredictCases
from tests.runner import clear_db

class TestPredictCasesEndpoints(TestCase):
    def setUp(self):
        self.app_context = app.test_request_context()
        self.app_context.push()
        self.client = app.test_client()
        self.app = app
        db.create_all()
        self.db = db

    def tearDown(self):
        clear_db(self.db)

    def test_return_all_predict_cases(self):
        PredictCases().save(self.db.session, id=1, state='RS', date=datetime.date(2020,1,1),
                            predictcases= 10, update=datetime.date(2020,1,1))
        PredictCases().save(self.db.session, id=2, state='SP', date=datetime.date(2020, 1, 2),
                            predictcases=30, update=datetime.date(2020, 1, 2))
        self.db.session.commit()


        resp = self.client.get('/data_api/v1/cases/predict_cases')
        response = json.loads(resp.get_data(as_text=True))

        self.assertEqual(len(response), 2)
        self.assertEqual(resp.status_code, 200)

    def test_return_404_when_predict_cases_empty(self):
        resp = self.client.get('/data_api/v1/cases/predict_cases')

        self.assertEqual(resp.status_code, 404)
