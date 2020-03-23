from flask_restplus import Namespace, Resource
from apis.data.services import ReportService
from flask import request
from flask_jwt_extended import jwt_required


data_endpoints = Namespace('data', description='Data related operations')

headers = data_endpoints.parser()
headers.add_argument(
    'Authorization',
    location='headers',
    required=True,
    help="Access token. E.g.: Bearer [JWT]"
)


@data_endpoints.route('/state/<string:state_code>')
@data_endpoints.expect(headers)
class GetStateCases(Resource):
    @jwt_required
    @data_endpoints.doc('by_state')
    def get(self, state_code):
        """Get confirmed, suspects, recovered and
        death cases for a given state"""
        return ReportService().search_city_cases_by_state(state_code)


@data_endpoints.route('/all')
@data_endpoints.expect(headers)
class GetAllCases(Resource):
    @jwt_required
    @data_endpoints.doc('all')
    def get(self):
        """Get all confirmed, suspects, recovered and
        death cases"""
        return ReportService().get_all_city_cases()


@data_endpoints.route('/search/<string:term>')
@data_endpoints.expect(headers)
class GetCasesFromTerm(Resource):
    @jwt_required
    def get(self, term):
        """Get all confirmed, suspects, recovered and
        death cases for a given term"""
        return ReportService().search_on_location_by_term(term)


@data_endpoints.route('/cases_location')
@data_endpoints.expect(headers)
class GetCasesNearLocation(Resource):
    @jwt_required
    def get(self):
        latitude = request.args.get('lat', None)
        longitude = request.args.get('lng', None)
        "Obter um array de casos de COVID-19 " \
            "próximos a latitude e long do usuario"
        return ReportService().get_cases_near_location(latitude, longitude)


def bind(api):
    api.add_namespace(data_endpoints)
