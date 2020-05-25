from unittest import TestCase
from app import app, db
from models import DataSus
from tests.runner import clear_db
import datetime


class TestDataSusMethods(TestCase):

    def setUp(self):
        self.app_context = app.test_request_context()
        self.app_context.push()
        app.test_client()
        self.app = app
        db.create_all()
        self.db = db

    def tearDown(self):
        clear_db(self.db)

    def test_if_save_method_saves_datasus_on_database(self):
        DataSus().save(self.db.session, region='Sudeste', state='SP', coduf=1,
                       city="São Paulo", date=datetime.date.today(),
                       newcases=1, totalcases=10, newdeaths=1, totaldeaths=2,
                       update=datetime.datetime.now(), codmun=1,
                       codhealthregion=100, namehealthregion='Região',
                       epiweek=20, population=10000000,
                       recoverednew=5, accompanyingnew=3)
        self.db.session.commit()
        _model = self.db.session.query(
            DataSus).filter_by(state='SP').first()
        self.assertIsNotNone(_model)
