from unittest import TestCase
from mock import patch
from app import app
from apis.auth.services import (create_tokens, refresh_access_token)
from custom_exceptions.auth_exceptions import BadUsernameOrPassword


class TestAuthServices(TestCase):

    def setUp(self):
        self.app_context = app.test_request_context()
        self.app_context.push()
        self.client = app.test_client()
        self.app = app

    def test_should_return_tokens_for_valid_credentials(self):
        tokens_data = create_tokens({
            'username': self.app.config['AUTH_USERNAME'],
            'password': self.app.config['AUTH_PASSWORD']
        })
        self.assertIsNotNone(tokens_data)

    def test_should_raise_baq_request_exception_for_invalid_username(self):
        with self.assertRaises(BadUsernameOrPassword):
            create_tokens({
                'username': 'some_invalid_user_name',
                'password': self.app.config['AUTH_PASSWORD']
            })

    def test_should_raise_baq_request_exception_for_invalid_password(self):
        with self.assertRaises(BadUsernameOrPassword):
            create_tokens({
                'username': self.app.config['AUTH_USERNAME'],
                'password': 'some_invalid_password'
            })

    @patch('apis.auth.services.get_jwt_identity')
    def test_should_refresh_access_token(self, mock_jwt_identity):
        mock_jwt_identity.return_value = 'user1'
        token_data = refresh_access_token()
        self.assertIsNotNone(token_data)
