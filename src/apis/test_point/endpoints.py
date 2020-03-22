from flask_restplus import Namespace, Resource
from apis.test_point.services import TestPointService
from flask import request

my_api = Namespace('test_point', description='Test point related operations')


@my_api.route('/all')
class GetAllTestPoints(Resource):
    @my_api.doc('all')
    def get(self):
        """Get all test points"""
        return TestPointService.getAll(self)

@my_api.route('/city/<string:city>')
class GetTestPointsByCity(Resource):
    @my_api.doc('by_city')
    def get(self, city):
        """Get tests points by city"""
        return TestPointService.getByCity(self,city)


def bind(api):
    api.add_namespace(my_api)
