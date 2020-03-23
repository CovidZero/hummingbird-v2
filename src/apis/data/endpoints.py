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


@data_endpoints.route('/state/<string:uf>')
@data_endpoints.expect(headers)
class GetStateSituation(Resource):
    @jwt_required
    @data_endpoints.doc('by_state')
    def get(self, uf):
        """Obter todos os casos confirmados, suspeitos,
        recuperados e óbitos de um Estado"""
        return ReportService().search_city_cases_by_state(uf)


@data_endpoints.route('/all')
@data_endpoints.expect(headers)
class GetAllCases(Resource):
    @jwt_required
    @data_endpoints.doc('all')
    def get(self):
        """Obter todos os casos confirmados, suspeitos,
        recuperados e óbitos"""
        return ReportService().get_all_city_cases()


@data_endpoints.route('/search')
@data_endpoints.expect(headers)
class GetCasesFromSearch(Resource):
    @jwt_required
    def get(self):
        """Obter todos os casos confirmados, suspeitos, recuperados
        e óbitos por cidade baseados em pesquisa pelo termo"""
        query = request.args.get('query')
        return ReportService().search_city_cases(query)


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
