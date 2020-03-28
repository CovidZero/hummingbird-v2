from flask_restplus import Namespace, Resource
from apis.test_point.services import TestPointService

test_point_endpoints = Namespace(
    'test_point',
    description='Test point related operations'
)


headers = test_point_endpoints.parser()
headers.add_argument(
    'Authorization',
    location='headers',
    required=True,
    help="Access token. E.g.: Bearer [JWT]"
)


@test_point_endpoints.route('/all', doc=False)
class GetAllTestPoints(Resource):
    @test_point_endpoints.doc('all')
    def get(self):
        """Get all test points"""
        return TestPointService().get_all()


@test_point_endpoints.route('/city/<string:city>', doc=False)
class GetTestPointsByCity(Resource):
    @test_point_endpoints.doc('by_city')
    def get(self, city):
        """Get tests points by city"""
        return TestPointService().get_by_city(city)


def bind(api):
    api.add_namespace(test_point_endpoints)
