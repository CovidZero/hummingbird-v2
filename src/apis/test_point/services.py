from flask import jsonify

from models import TestPoint


class TestPointService:

    def getAll(self):
        test_points = TestPoint.query.all()
        return jsonify([i.serialize for i in test_points])

    def getByCity(self, city):
        test_points = TestPoint.query.filter_by(city=city).all()
        return jsonify([i.serialize for i in test_points])
