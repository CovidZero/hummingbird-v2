from flask_restplus import Namespace, Resource, fields
from apis.data.services import ReportService
from apis.data import state_services


data_endpoints = Namespace('data', description='Data related operations')

headers = data_endpoints.parser()
headers.add_argument(
    'Authorization',
    location='headers',
    required=True,
    help="Access token. E.g.: Bearer [JWT]"
)

cases_detail_response = data_endpoints.model(
    'State Cases Detail Response',
    {
        'totalCases': fields.Integer(required=True,
                                     description='Total active cases'),
        'deaths': fields.Integer(required=True,
                                 description='Total deaths')
    }
)

all_state_cases_response = data_endpoints.model('State Cases Response', {
    'stateCode': fields.String(required=True, description='State code'),
    'stateName': fields.String(required=True, description='State name'),
    'lat': fields.String(required=True, description='State Latitude'),
    'lng': fields.String(required=True, description='State Longitude'),
    'cases': fields.Nested(cases_detail_response,
                           required=True, description='Cases details'),
})

sum_all_cases_response = data_endpoints.model('Sum All Cases Response', {
    'totalCases': fields.String(required=True, description='Total cases'),
    'totalCasesMS': fields.String(required=True,
                                  description='Total cases confirmed by MS'),
    'deaths': fields.String(required=True, description='Deaths'),
})


@data_endpoints.route('/state/cases/all')
@data_endpoints.expect(headers)
class GetAllStateCases(Resource):
    @data_endpoints.doc('state_cases_all')
    @data_endpoints.marshal_with(all_state_cases_response)
    def get(self):
        """Get cases from all states"""
        return state_services.get_all_state_cases()


@data_endpoints.route('/all')
@data_endpoints.expect(headers)
class GetAllCases(Resource):
    @data_endpoints.doc('all')
    @data_endpoints.marshal_with(sum_all_cases_response)
    def get(self):
        """Get all confirmed, suspects, recovered and
        death cases"""
        return state_services.get_sum_state_cases()


@data_endpoints.route('/city/cases/all')
@data_endpoints.expect(headers)
class GetAllCityCases(Resource):
    def get(self):
        """Get all confirmed, suspects, recovered and
        death cases"""
        return ReportService().get_all_city_cases()


@data_endpoints.route('/search/<string:term>')
@data_endpoints.expect(headers)
class GetCasesFromTerm(Resource):
    def get(self, term):
        """Get all confirmed, suspects, recovered and
        death cases for a given term"""
        return ReportService().search_on_location_by_term(term)


def bind(api):
    api.add_namespace(data_endpoints)
