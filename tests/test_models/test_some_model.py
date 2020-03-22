from unittest import TestCase
from app import app, db
from models import SomeModel
from tests.runner import clear_db


class TestTransferModel(TestCase):

    def setUp(self):
        self.app_context = app.test_request_context()
        self.app_context.push()
        app.test_client()
        self.app = app
        db.create_all()
        self.db = db

    def tearDown(self):
        clear_db(self.db)

    def test_if_create_method_saves_some_model_on_database(self):
        SomeModel().save(self.db.session, id='hummingbird', name='No Covid')
        self.db.session.commit()
        _model = self.db.session.query(SomeModel).filter_by(id='hummingbird').first()
        self.assertIsNotNone(_model)


