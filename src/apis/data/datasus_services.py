from app import db
from models import DataSus

from sqlalchemy import func


def get_sus_list(page):
    try:
        if page:
            sus_list, pagination = DataSus().fetch_paginated(db.session, page)
        else:
            sus_list = DataSus().fetch_all(db.session)
            pagination = {}

        return {
            'sus_list': sus_list,
            'pagination': pagination
        }
    finally:
        db.session.close()


def get_graph_last_30_days():
    try:
        last_30_days = DataSus.query.filter(DataSus.region == 'Brasil') \
            .with_entities(DataSus.date, DataSus.totalcases,
                           DataSus.totaldeaths) \
            .order_by(DataSus.date.desc()).limit(30).all()

        result = []
        for day in last_30_days:
            current_date = {
                'date': day.date,
                'totalCases': day.totalcases,
                'totalDeaths': day.totaldeaths
            }
            result.append(current_date)

        return result
    finally:
        db.session.close()


def get_regions():
    try:
        subquery = DataSus.query.with_entities(
            func.max(DataSus.date)).subquery()
        regions = DataSus.query.filter(DataSus.date == subquery) \
            .with_entities(DataSus.id, DataSus.region, DataSus.state,
                           DataSus.city, DataSus.coduf, DataSus.codmun,
                           DataSus.population, DataSus.date,
                           DataSus.totalcases, DataSus.population,
                           DataSus.date, DataSus.totalcases,
                           DataSus.totaldeaths) \
            .all()

        result = []
        for region in regions:
            current_region = {
                'id': region.id,
                'region': region.region,
                'state': region.state,
                'city': region.city,
                'coduf': region.coduf,
                'codmun': region.codmun,
                'population': region.population,
                'date': region.date,
                'totalCases': region.totalcases,
                'totalDeaths': region.totaldeaths
            }
            result.append(current_region)

        return result
    finally:
        db.session.close()
