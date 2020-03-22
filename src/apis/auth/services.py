from app import app
from custom_exceptions.auth_exceptions import BadUsernameOrPassword
from flask_jwt_extended import (
    create_access_token, create_refresh_token, get_jwt_identity
)


def create_tokens(data):
    if data['username'] != app.config['AUTH_USERNAME'] or \
            data['password'] != app.config['AUTH_PASSWORD']:
        raise BadUsernameOrPassword()
    access_token = create_access_token(identity=data['username'])
    refresh_token = create_refresh_token(identity=data['username'])
    return {'access_token': access_token, 'refresh_token': refresh_token,
            'expires': app.config['JWT_ACCESS_TOKEN_EXPIRES']}


def refresh_access_token():
    current_user = get_jwt_identity()
    return {'access_token': create_access_token(identity=current_user),
            'expires': app.config['JWT_ACCESS_TOKEN_EXPIRES']}
