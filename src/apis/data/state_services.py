from app import db
from models import StateCases


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
        "activeCases": state_case.totalcases,
        "deaths": state_case.deaths
    }
