from flask_seeder import Seeder, Faker, generator
from models import City


class CityCasesSeeder(Seeder):

    def run(self):

        faker_for_city = Faker(
            cls=City,
            init={
                'id': generator.Sequence(start=1, end=1000),
                'ibge_id': generator.Integer(start=300000, end=399999),
                'country': 'Brazil',
                'city': 'Test',
                'deaths': 1,
                'state_id': generator.Integer(start=2, end=28),
                'totalcases': generator.Integer(start=1, end=10)

            }
        )

        for case in faker_for_city.create(500):
            print("Adding city case: %s" % case)
            self.db.session.add(case)


