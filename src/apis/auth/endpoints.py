from flask_restplus import Namespace, Resource, fields
from apis.auth.services import create_tokens
from apis.auth.services import refresh_access_token
from flask_jwt_extended import jwt_refresh_token_required


auth_endpoints = Namespace(
    'authorization',
    description='Endpoint operations related to Authorization Tokens.'
)


create_tokens_request = auth_endpoints.model(
    'Create Tokens Request', {
        'username': fields.String(
            required=True,
            description='Username to be identified in authentication process'
        ),
        'password': fields.String(
            required=True,
            description='Password related to the username'
        )
    }
)

create_tokens_response = auth_endpoints.model(
    'Create Tokens Response', {
        'access_token': fields.String(
            required=True,
            description='Access token to be used for all requests'),
        'refresh_token': fields.String(
            required=True,
            description='Refresh token to be used to get a new access token'),
        'expires': fields.Integer(
            required=True,
            description='Token time in seconds')
    }
)

refresh_access_token_response = auth_endpoints.model(
    'Refresh Access Token Response', {
        'access_token': fields.String(
            required=True,
            description='Access token to be used for all requests'
        ),
        'expires': fields.Integer(
            required=True,
            description='Token time in seconds'
        )
    }
)

headers = auth_endpoints.parser()
headers.add_argument('Authorization', location='headers', required=True,
                     help="Refresh token. E.g.: Bearer [JWT]")

docs = {
    'get_tokens': '<p>Gets a new access token to be used '
                  'as an authorization header value for '
                  'all other endpoints and a refresh token '
                  'to be used to get a new access token.</p>',
    'refresh_access_token': '<p>Gets a new access token to be '
                            'used as an authorization header '
                            'value for all other endpoints.</p>'
}


@auth_endpoints.route('/create_tokens',
                      doc={"description": docs['get_tokens']})
class CreateTokens(Resource):
    @auth_endpoints.doc('access_token')
    @auth_endpoints.expect(create_tokens_request, validate=True)
    @auth_endpoints.marshal_with(create_tokens_response)
    def post(self):
        """Create Access and Refresh token"""
        return create_tokens(auth_endpoints.payload)


@auth_endpoints.route('/refresh_access_token',
                      doc={"description": docs['refresh_access_token']})
@auth_endpoints.expect(headers)
class RefreshAccessToken(Resource):
    @jwt_refresh_token_required
    @auth_endpoints.doc('refresh_token')
    @auth_endpoints.marshal_with(refresh_access_token_response)
    def get(self):
        """Refresh access token"""
        return refresh_access_token()


def bind(api):
    api.add_namespace(auth_endpoints)
