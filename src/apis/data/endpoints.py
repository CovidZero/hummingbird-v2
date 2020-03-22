from flask_restplus import Namespace, Resource
from apis.data.services import ReportService
from flask import request

my_api = Namespace('data', description='Data related operations')


@my_api.route('/state/<string:uf>')
class GetStateSituation(Resource):
    @my_api.doc('by_state')
    def get(self, uf):
        """Obter todos os casos confirmados, suspeitos,
        recuperados e óbitos de um Estado"""
        return ReportService().search_city_cases_by_state(uf)


@my_api.route('/all')
class GetAllCases(Resource):
    @my_api.doc('all')
    def get(self):
        """Obter todos os casos confirmados, suspeitos,
        recuperados e óbitos"""
        return ReportService().get_all_city_cases()


@my_api.route('/search')
class GetCasesFromSearch(Resource):
    def get(self):
        """Obter todos os casos confirmados, suspeitos, recuperados
        e óbitos por cidade baseados em pesquisa pelo termo"""
        query = request.args.get('query')
        return ReportService().search_city_cases(query)


@my_api.route('/cases_location')
class GetCasesNearLocation(Resource):
    def get(self):
        latitude = request.args.get('lat', None)
        longitude = request.args.get('lng', None)
        "Obter um array de casos de COVID-19 " \
            "próximos a latitude e long do usuario"
        return ReportService().get_cases_near_location(latitude, longitude)


def bind(api):
    api.add_namespace(my_api)
