from flask_seeder import Seeder, Faker, generator
from models import City


class CityCasesSeeder(Seeder):

    def run(self):
        _id = generator.Sequence()

        faker_for_city = Faker(
            cls=City,
            init={
                'id': _id,
                'country': 'Brazil',
                'city': 'Test',
                'state_id': generator.Integer(start=2, end=28),
                'totalcases': generator.Integer(start=1, end=10)

            }
        )

        for state in faker_for_city.create(100):
            print("Adding city case: %s" % state)
            self.db.session.add(state)


