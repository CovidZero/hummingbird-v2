from models import City
from sqlalchemy.sql import or_

class ReportService():

    def searchCityCases(self, query):
        cases = City.query.filter(or_(City.city.like('%'+query+'%'), City.state.like('%'+query+'%'))).all()

        result = []

        for case in cases:
            activeCases = case.total_cases - case.suspects - case.refuses - case.deaths - case.recovered
            currentCase = {
            'city': case.city,
            'state': case.state,
            'cases': {
                'activeCases': activeCases,
                'suspectedCases': case.suspects,
                'recoveredCases': case.recovered,
                'deaths': case.deaths
            }}
            result.append(currentCase)

        return result
    
    def getAllCityCases(self):
        todos_cases = City.query.all()

        return compileCases(todos_cases)

    def searchCityCasesByState(self, uf):
        citySituation = City.query.filter_by(
            state=uf).all()

        return compileCases(citySituation)



def compileCases(data):
    activeCases = sum([(city.total_cases - city.suspects - city.refuses -
                    city.deaths - city.recovered) for city in data]) or 0
    suspectedCases = sum(
        [city.suspects for city in data]) or 0
    recoveredCases = sum(
        [city.recovered for city in data]) or 0
    deaths = sum([city.deaths for city in data]) or 0

    return {
        'activeCases': activeCases,
        'suspectedCases': suspectedCases,
        'recoveredCases': recoveredCases,
        'deaths': deaths
    }