from models import TestPoint

class TestPointService():
    
    def getAll(self):
        test_points = TestPoint.query.all()
        return test_points
    
    def getByCity(self, city):
        test_points = TestPoint.query.filter_by(city=city).all()
        return test_points
