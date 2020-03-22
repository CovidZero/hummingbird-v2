from flask_restplus import Namespace, Resource
from apis.test_point.services import TestPointService
from flask import request

my_api = Namespace('test_point', description='Test point related operations')


@my_api.route('/all')
class GetAllCases(Resource):
    @my_api.doc('all')
    def get(self):
        """Obter todos os casos confirmados, suspeitos, recuperados e óbitos"""
        return TestPointService.getAll(self)

@my_api.route('/city/<string:city>')
class GetStateSituation(Resource):
    @my_api.doc('by_city')
    def get(self, city):
        """Get all tests_points from city"""
        return TestPointService.getByCity(self,city)


def bind(api):
    api.add_namespace(my_api)
