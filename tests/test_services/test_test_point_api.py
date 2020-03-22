import json
from unittest import TestCase
from app import app, db
from models import TestPoint
from tests.runner import clear_db

class TestTestPointApi(TestCase):

    def setUp(self):
        self.app_context = app.test_request_context()
        self.app_context.push()
        self.client = app.test_client()
        self.app = app
        db.create_all()
        self.db = db

    def tearDown(self):
        clear_db(self.db)

    def test_get_all_test_points(self):

        # Generate test data
        TestPoint().save(self.db.session, name="Hospital1",address="Rua 1",city="São Paulo",
            zip_code = "13547895", latitude = -23.112571, longitude = -50.23952)

        TestPoint().save(self.db.session, name="Hospital1",address="Rua 1",city="city123",
            zip_code = "13547895", latitude = -23.112571, longitude = -50.23952)

        self.db.session.commit()

        resp = self.client.get('/data_api/v1/test_point/all')
        data = json.loads(resp.get_data(as_text=True))

        assert len(data) == 2

    def test_get_test_points_by_city(self):
        # Generate test data
        TestPoint().save(self.db.session, name="Hospital1",address="Rua 1",city="São Paulo",
            zip_code = "13547895", latitude = -23.112571, longitude = -50.23952)

        TestPoint().save(self.db.session, name="Hospital1",address="Rua 1",city="city123",
            zip_code = "13547895", latitude = -23.112571, longitude = -50.23952)

        self.db.session.commit()

        resp = self.client.get('/data_api/v1/test_point/city/city123')
        data = json.loads(resp.get_data(as_text=True))

        assert len(data) == 1

    def test_test_points_not_found(self):

            resp = self.client.get('/data_api/v1/test_point/city/city_not_exist')
            data = json.loads(resp.get_data(as_text=True))

            assert len(data) == 0