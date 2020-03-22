from flask import Blueprint
from flask_restplus import Api as ApiRestPlus
from apis.auth import endpoints as auth_endpoints
from apis.data import endpoints as data_endpoints
from apis.test_point import endpoints as test_point_endpoints


client_api = ApiRestPlus(
    Blueprint('Data API', __name__),
    title='Data API',
    version='1.0',
    description='Endpoints to serve data to front end clients'
)

# Bind each namespace for data here
auth_endpoints.bind(client_api)
data_endpoints.bind(client_api)
test_point_endpoints.bind(client_api)


def load_apis(app):
    app.register_blueprint(
        client_api.blueprint, url_prefix='/data_api/v1'
    )
