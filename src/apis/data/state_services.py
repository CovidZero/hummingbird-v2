from app import db
from models import StateCases
from models import StateCasesPerDay
from sqlalchemy import func
from util import date_parser


def get_state_cases():
    try:
        state_cases = StateCases().fetch_all(db.session)
        result = []
        for case in state_cases:
            result.append({
                "stateCode": case.state_data.abbreviation,
                "stateName": case.state_data.name,
                "lat": case.state_data.lat,
                "lng": case.state_data.lng,
                "cases": compile_state_cases(case)
            })
        return result

    finally:
        db.session.close()


def get_daily_state_cases(page):
    try:
        daily_state_cases, pagination = \
            StateCasesPerDay().fetch_paginated(db.session, page)
        cases = []
        for c in daily_state_cases:
            cases.append({
                "stateCode":
                    c.state_data.abbreviation if c.state_data else None,
                "stateName":
                    c.state_data.name if c.state_data else None,
                "lat":
                    c.state_data.lat if c.state_data else None,
                "lng":
                    c.state_data.lng if c.state_data else None,
                "country": c.country,
                "date": date_parser.datetime_to_str(c.date),
                "case_detail": {
                    "newCases": c.newcases,
                    "totalCases": c.totalcases
                }
            })
        return {
            'cases': cases,
            'pagination': pagination,
        }
    finally:
        db.session.close()


def compile_state_cases(state_case):
    return {
        "totalCases": state_case.totalcases,
        "deaths": state_case.deaths
    }


def compile_daily_state_cases(state_case):
    return {
        "totalCases": state_case.totalcases,
        "deaths": state_case.deaths
    }


def get_sum_state_cases():
    return {
        "totalCases": get_sum(StateCases.totalcases),
        "totalCasesMS": get_sum(StateCases.totalcasesms),
        "deaths": get_sum(StateCases.deaths)
    }


def get_sum(cases):
    return db.session.query(func.sum(cases)).first()[0]
