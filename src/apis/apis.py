from flask import Blueprint
from flask_restplus import Api as ApiRestPlus
from apis.data import endpoints as data_endpoints


client_api = ApiRestPlus(
    Blueprint('Data API', __name__),
    title='Data API',
    version='1.0',
    description='Endpoints to serve data to front end clients'
)

# Bind each namespace for data here
data_endpoints.bind(client_api)
# Bind each namespace for data here


def load_apis(app):
    app.register_blueprint(client_api.blueprint, url_prefix='/data_api/v1')

