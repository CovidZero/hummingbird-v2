import json
from unittest import TestCase
from app import app


class TestAuthEndpoints(TestCase):

    def setUp(self):
        self.app_context = app.test_request_context()
        self.app_context.push()
        self.client = app.test_client()
        self.app = app

    def test_should_create_tokens_for_valid_credentials(self):
        response = self.client.post(
            '/data_api/v1/authorization/create_tokens',
            json={"username": self.app.config['AUTH_USERNAME'], "password": self.app.config['AUTH_PASSWORD']}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data.get('access_token'))
        self.assertIsNotNone(data.get('refresh_token'))
        self.assertIsNotNone(data.get('expires'))

    def test_should_raise_unauthorized_status_code_for_invalid_credentials(self):
        response = self.client.post(
            '/data_api/v1/authorization/create_tokens',
            json={"username": self.app.config['AUTH_USERNAME'], "password": 'some_invalid_password'}
        )
        self.assertEqual(response.status_code, 401)
