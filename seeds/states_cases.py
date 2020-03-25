from flask_seeder import Seeder, Faker, generator
from models import StateCases


class StatePerDaySeeder(Seeder):

    def run(self):
        _id = generator.Sequence()
        __id = generator.Sequence()

        faker_for_state = Faker(
            cls=StateCases,
            init={
                'id': _id,
                'state': __id,
                'totalcases': generator.Integer(start=10, end=20),
                'totalcasesms': generator.Integer(start=1, end=10),
                'notconfirmedbyms': generator.Integer(start=1, end=10),
                'deaths': generator.Integer(start=0, end=2),
                'url': 'https://someurl.com.br'

            }
        )

        faker_for_total = Faker(
            cls=StateCases,
            init={
                'id': _id,
                'state': __id,
                'totalcases': 100,
                'totalcasesms': 50,
                'notconfirmedbyms': 50,
                'deaths': 10,
                'url': 'https://someurl.com.br'

            }
        )

        for state in faker_for_total.create(1):
            print("Adding state case: %s" % state)
            self.db.session.add(state)

        for state in faker_for_state.create(27):
            print("Adding state case: %s" % state)
            self.db.session.add(state)
