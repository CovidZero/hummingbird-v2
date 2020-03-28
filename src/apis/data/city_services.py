from app import db
from models import City


def get_city_cases(page):
    try:
        # TODO: unitests
        if page:
            city_cases, pagination = City().fetch_paginated(db.session, page)
        else:
            city_cases = City().fetch_all(db.session)
            pagination = {}
        cases = []
        for c in city_cases:
            cases.append({
                'city': c.city,
                'ibge_id': c.ibge_id,
                'country': c.country,
                'state_id': c.state_id,
                'totalcases': c.totalcases
            })
        return {
            'cases': cases,
            'pagination': pagination,
        }
    finally:
        db.session.close()
