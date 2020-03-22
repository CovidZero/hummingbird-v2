from flask_restplus import Namespace, Resource
from models import City
from sqlalchemy.sql import func

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
        situacao_cidades = City.query.filter_by(
            state=sigla).all()

        activeCases = sum([(cidade.total_cases - cidade.suspects - cidade.refuses -
                            cidade.deaths - cidade.recovered) for cidade in situacao_cidades]) or 0
        suspectedCases = sum(
            [cidade.suspects for cidade in situacao_cidades]) or 0
        recoveredCases = sum(
            [cidade.recovered for cidade in situacao_cidades]) or 0
        deaths = sum([cidade.deaths for cidade in situacao_cidades]) or 0

        return {
            'activeCases': activeCases,
            'suspectedCases': suspectedCases,
            'recoveredCases': recoveredCases,
            'deaths': deaths
        }


def bind(api):
    api.add_namespace(my_api)
