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


@my_api.route('/state/<string:sigla>')
class GetStateSituation(Resource):
    @my_api.doc('by_state')
    def get(self, sigla):
        """Obter todos os casos confirmados, suspeitos, recuperados e óbitos de um Estado"""
        return ReportService.searchCityCasesByState(self,sigla)

@my_api.route('/all')
class GetAllCases(Resource):
    @my_api.doc('all')
    def get(self):
        """Obter todos os casos confirmados, suspeitos, recuperados e óbitos"""
        return ReportService.getAllCityCases(self)

@my_api.route('/search/<string:termo>')
class GetCasesFromSearch(Resource):
    def get(self, termo):
        """Obter todos os casos confirmados, suspeitos, recuperados e óbitos por cidade baseados em pesquisa pelo termo"""
        return ReportService.searchCityCases(self, termo)






def bind(api):
    api.add_namespace(my_api)
