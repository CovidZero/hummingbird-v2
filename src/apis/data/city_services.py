from app import db
from models import City

RESTRAINED_CITIES = [
    'NÃO ESPECIFICADA',
    'FORA DO ESTADO',
    'ESTRANGEIRO',
    'INDEFINIDA',
    'CASO SEM LOCALIZAÇÃO DEFINIDA'
]


def get_city_cases(page):
    try:
        if page:
            city_cases, pagination = City().fetch_paginated(db.session, page)
        else:
            city_cases = City().fetch_all(db.session)
            pagination = {}
        cases = []
        for c in city_cases:
            if c.city not in RESTRAINED_CITIES:
                cases.append({
                    'id': c.id,
                    'city': c.city,
                    'ibge_id': c.ibge_id,
                    'country': c.country,
                    'state_id': c.state_id,
                    'totalcases': c.totalcases,
                    'deaths': c.deaths
                })
        return {
            'cases': cases,
            'pagination': pagination,
        }
    finally:
        db.session.close()


def search_on_location_by_term(query):
    global current_case
    cases = City.query.filter((City.city.like(query))).all()

    result = []

    for case in cases:
        if case.city not in RESTRAINED_CITIES:
            current_case = {
                'city': case.city,
                'state': case.state_data.name,
                'cases': {
                    'totalCases': case.totalcases,
                    'deaths': case.deaths
                }
            }
        result.append(current_case)

    return result


def get_totals_cases_per_city():
    all_cases = City.query.all()
    return compile_cases(all_cases)


def compile_cases(data):
    total_cases = sum(
        [city.totalcases
         for city in data]) or 0
    deaths = sum(
        [city.deaths
         for city in data]) or 0

    return {
        'totalCases': total_cases,
        'deaths': deaths
    }
