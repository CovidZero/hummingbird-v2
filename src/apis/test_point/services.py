from flask import jsonify

from models import TestPoint


class TestPointService:

    def get_all(self):
        test_points = TestPoint.query.all()
        return jsonify([i.serialize for i in test_points])

    def get_by_city(self, city):
        test_points = TestPoint.query.filter_by(city=city).all()
        return jsonify([i.serialize for i in test_points])
