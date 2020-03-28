from flask_restplus import Namespace, Resource, fields
from apis.data.services import ReportService
from apis.data import state_services
from apis.data import city_services


data_endpoints = Namespace('cases', description='Cases related operations')

headers = data_endpoints.parser()
headers.add_argument(
    'Authorization',
    location='headers',
    required=True,
    help="Access token. E.g.: Bearer [JWT]"
)

city_cases = data_endpoints.model('City Cases', {
    'id': fields.Integer(required=True, description='Id'),
    'city': fields.String(required=True, description='City'),
    'country': fields.String(required=True, description='Country'),
    'state_id': fields.Integer(required=True, description='State Id'),
    'totalcases': fields.Integer(required=True, description='Total cases'),

})

pages_info = data_endpoints.model('Pages Info', {
    'total_pages': fields.Integer(
        required=False, description='Total Pages'),
    'has_next': fields.Boolean(
        required=False, description='Has next page?'),
    'has_previous': fields.Boolean(
        required=False, description='Has previous page?'),
    'next_page': fields.Integer(
        required=False, description='Next page'),
    'current_page': fields.Integer(
        required=False, description='Current page')

})

city_cases_response_list = data_endpoints.model('City Cases Response List', {
    'cases': fields.Nested(
        city_cases, required=True, as_list=True,  description='Cases'),
    'page_info': fields.Nested(
        pages_info, required=True, description='Pages info')
})

city_cases_response_report = data_endpoints.model(
    'City Cases Response Report', {
        'totalCases': fields.Integer(
            required=True, description='Total cases')
    }
)

city_cases_response_list_report = data_endpoints.model(
    'City Cases Response List Report', {
        'totalCases': fields.Integer(
            required=True, description='Total cases')
    }
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

# TODO: should be mapped as a list
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


@data_endpoints.route('/state')
class ListStateCases(Resource):
    @data_endpoints.doc('state_cases')
    @data_endpoints.marshal_with(all_state_cases_response)
    def get(self):
        """List cases per state"""
        return state_services.get_state_cases()


@data_endpoints.route('/state/report')
class GetStateCasesTotals(Resource):
    @data_endpoints.doc('state_report_cases')
    @data_endpoints.marshal_with(sum_all_cases_response)
    def get(self):
        """Cases per state report"""
        return state_services.get_sum_state_cases()


@data_endpoints.route('/city')
class CityCasesList(Resource):
    # TODO: has no tests
    @data_endpoints.doc('city_cases_list')
    @data_endpoints.marshal_with(city_cases_response_list)
    def get(self):
        """Cases per city list"""
        return city_services.get_city_cases(None)


@data_endpoints.route('/city/<int:page>')
class CityCasesPaginatedList(Resource):
    # TODO: has no tests
    @data_endpoints.doc('city_cases_paginated_list')
    @data_endpoints.marshal_with(city_cases_response_list)
    def get(self, page):
        """Cases per city list paginated"""
        return city_services.get_city_cases(page)


@data_endpoints.route('/city/report')
class CityCasesReport(Resource):
    # TODO: has no tests
    @data_endpoints.doc('city_cases_report')
    @data_endpoints.marshal_with(city_cases_response_report)
    def get(self):
        """Cases per city report"""
        return ReportService().get_totals_cases_per_city()


@data_endpoints.route('/city/<string:term>/report')
class GetCityCasesTotalsFiltered(Resource):
    # TODO: has no tests
    def get(self, term):
        """Cases per city report, filtered by city term"""
        return ReportService().search_on_location_by_term(term)


def bind(api):
    api.add_namespace(data_endpoints)
