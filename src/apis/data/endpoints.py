from flask_restplus import Namespace, Resource, fields
from apis.data.services import ReportService
from apis.data import state_services
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

cases_detail_response = data_endpoints.model('State Cases Detail Response', {
    'activeCases': fields.Integer(required=True,
                                  description='Total active cases'),
    'deaths': fields.Integer(required=True,
                             description='Total deaths')
})


state_cases_response = data_endpoints.model('State Cases Response', {
    'stateCode': fields.String(required=True, description='State code'),
    'stateName': fields.String(required=True, description='State name'),
    'lat': fields.String(required=True, description='State Latitude'),
    'long': fields.String(required=True, description='State Longitude'),
    'cases': fields.Nested(cases_detail_response,
                           required=True, description='Cases details'),
})


@data_endpoints.route('/state/<string:state_code>')
@data_endpoints.expect(headers)
class GetCityCasesByState(Resource):
    @data_endpoints.doc('by_state')
    def get(self, state_code):
        """Get confirmed, suspects, recovered and
        death cases for a given state"""
        return ReportService().search_city_cases_by_state(state_code)


@data_endpoints.route('/state/cases/all')
@data_endpoints.expect(headers)
class GetAllStateCases(Resource):
    @data_endpoints.doc('state_cases_all')
    @data_endpoints.marshal_with(state_cases_response)
    def get(self):
        """Get cases from all states"""
        return state_services.get_all_state_cases()


@data_endpoints.route('/all')
@data_endpoints.expect(headers)
class GetAllCases(Resource):
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
        """Gets an array of COVID-19 cases near user latitude and longitude"""
        return ReportService().get_cases_near_location(
            latitude, longitude
        )


def bind(api):
    api.add_namespace(data_endpoints)
