from models import City


class ReportService:

    def search_on_location_by_term(self, query):
        cases = City.query.filter((City.city.like(query))).all()

        result = []

        for case in cases:
            current_case = {
                'city': case.city,
                'state': case.state_data.name,
                'cases': {
                    'totalCases': case.totalcases
                }
            }
            result.append(current_case)

        return result

    def get_all_city_cases(self):
        all_cases = City.query.all()
        return compile_cases(all_cases)


def compile_cases(data):
    total_cases = sum(
        [city.totalcases
            for city in data]) or 0

    return {'totalCases': total_cases}
