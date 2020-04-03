from datetime import date


def datetime_to_str(date_obj: date):
    return date_obj.strftime("%Y-%m-%d")
