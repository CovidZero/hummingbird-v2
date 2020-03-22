from flask_restplus import Namespace, Resource
from apis.data.services import ReportService

my_api = Namespace('data', description='Data related operations')


@my_api.route('/foo_bar')
class GetFooBar(Resource):
    @my_api.doc('foo_bar')
    def get(self):
        """Check Unique Payment"""
        status = True
        return {'ok': status}


@my_api.route('/state/<string:uf>')
class GetStateSituation(Resource):
    @my_api.doc('by_state')
    def get(self, uf):
        """Obter todos os casos confirmados, suspeitos, recuperados e óbitos de um Estado"""
        return ReportService.searchCityCasesByState(self,uf)

@my_api.route('/all')
class GetAllCases(Resource):
    @my_api.doc('all')
    def get(self):
        """Obter todos os casos confirmados, suspeitos, recuperados e óbitos"""
        return ReportService.getAllCityCases(self)

@my_api.route('/search/<string:query>')
class GetCasesFromSearch(Resource):
    def get(self, query):
        """Obter todos os casos confirmados, suspeitos, recuperados e óbitos por cidade baseados em pesquisa pelo termo"""
        return ReportService.searchCityCases(self, query)






def bind(api):
    api.add_namespace(my_api)
