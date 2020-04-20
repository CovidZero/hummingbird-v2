from app import db
from models import PredictCases


def get_predict_cases():
    try:
        result = PredictCases().fetch_all(db.session)
        return result
    finally:
        db.session.close()
