from flask_seeder import Seeder, Faker, generator
from models import StateCasesPerDay
from seeds.custom_generators import StateGeneratorRandom
from seeds.custom_generators import DateGenerator


class StatePerDaySeeder(Seeder):

    def run(self):
        _id = generator.Sequence()

        faker_for_state = Faker(
            cls=StateCasesPerDay,
            init={
                'id': _id,
                'date': DateGenerator('-15d', 'now'),
                'country': 'Brazil',
                'state_id': StateGeneratorRandom(),
                'newcases': generator.Integer(start=0, end=12),
                'totalcases': generator.Integer(start=10, end=20)

            }
        )

        faker_for_total = Faker(
            cls=StateCasesPerDay,
            init={
                'id': _id,
                'date': DateGenerator('-15d', 'now'),
                'country': 'Brazil',
                'state_id': 'TOTAL',
                'newcases': generator.Integer(start=0, end=12),
                'totalcases': generator.Integer(start=10, end=20)

            }
        )

        for state in faker_for_state.create(10):
            print("Adding state per day: %s" % state)
            self.db.session.add(state)

        for state in faker_for_total.create(10):
            print("Adding state per day: %s" % state)
            self.db.session.add(state)
