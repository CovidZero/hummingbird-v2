from app import db
from models import StateCases
from sqlalchemy import func


def get_all_state_cases():
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


def compile_state_cases(state_case):
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
