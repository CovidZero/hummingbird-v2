from app import db
from models import City


def get_city_cases(page):
    try:
        # TODO: unitests
        if page:
            city_cases, pages_info = City().fetch_paginated(db.session, page)
        else:
            city_cases = City().fetch_all(db.session)
            pages_info = {}
        cases = []
        for c in city_cases:
            cases.append({
                'city': c.city,
                'country': c.country,
                'state_id': c.state_id,
                'totalcases': c.totalcases
            })
        return {
            'cases': cases,
            'pages_info': pages_info,
        }
    finally:
        db.session.close()
