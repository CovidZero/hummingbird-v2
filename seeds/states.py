from flask_seeder import Seeder, Faker, generator
from models import State
from seeds.custom_generators import StateGeneratorSequence


class StateSeeder(Seeder):

    def run(self):
        _id = generator.Sequence()

        faker_for_state = Faker(
            cls=State,
            init={
                'id': _id,
                'country': 'Brazil',
                'state': StateGeneratorSequence(),
                'lat': "99.000",
                'long': "99.000",

            }
        )

        faker_for_total = Faker(
            cls=State,
            init={
                'id': _id,
                'country': 'Brazil',
                'state': 'Total',
                'lat': f"00.000",
                'long': f"00.000",

            }
        )

        for state in faker_for_total.create(1):
            print("Adding state: %s" % state)
            self.db.session.add(state)

        for state in faker_for_state.create(27):
            print("Adding state: %s" % state)
            self.db.session.add(state)
