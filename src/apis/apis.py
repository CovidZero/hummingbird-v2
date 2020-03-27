import os
from flask import Blueprint, url_for
from flask_restplus import Api as ApiRestPlus
from apis.auth import endpoints as auth_endpoints
from apis.data import endpoints as data_endpoints
from apis.test_point import endpoints as test_point_endpoints


class SecureApiRestPlus(ApiRestPlus):
    """
    Custom Flask Rest Plus API Class
    """

    @property
    def specs_url(self):
        """
        Method overwritten to force HTTPS on swagger static resources
        for specific environments
        :return:
        """
        scheme = 'https' if os.environ.get('FLASK_ENV') in \
            ['staging', 'production'] else 'http'
        return url_for(self.endpoint('specs'), _external=True, _scheme=scheme)


client_api = SecureApiRestPlus(
    Blueprint('Data API', __name__),
    title='Data API',
    version='1.0',
    description='Endpoints to serve data to front end clients'
)


# Bind each namespace here
auth_endpoints.bind(client_api)
data_endpoints.bind(client_api)
test_point_endpoints.bind(client_api)
# Bind each namespace here


def load_apis(app):
    app.register_blueprint(
        client_api.blueprint, url_prefix='/data_api/v1'
    )
