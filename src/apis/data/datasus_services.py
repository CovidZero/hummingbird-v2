from app import db
from models import DataSus


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
