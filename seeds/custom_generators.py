import random
from faker import Faker
from flask_seeder.generator import Generator


fake = Faker()


class StateGeneratorRandom(Generator):
    states = ["AC", "AL", "AP", "AM", "BA",
              "CE", "DF", "ES", "GO", "MA",
              "MT", "MS", "MG", "PA", "PB",
              "PR", "PE", "PI", "RJ", "RN",
              "RS", "RO", "RR", "SC", "SP",
              "SE", "TO"]

    def generate(self):
        return random.choice(self.states)


class StateGeneratorSequence(Generator):
    states = ["AC", "AL", "AP", "AM", "BA",
              "CE", "DF", "ES", "GO", "MA",
              "MT", "MS", "MG", "PA", "PB",
              "PR", "PE", "PI", "RJ", "RN",
              "RS", "RO", "RR", "SC", "SP",
              "SE", "TO"]

    current = 0

    def generate(self):
        s = self.states[self.current]
        if self.current >= 26:
            self.current = 0
        else:
            self.current += 1
        return s


class DateGenerator(Generator):

    def __init__(self, start, end):
        super(Generator, self).__init__()
        self._start = start
        self._end = end

    def generate(self):
        return fake.date_time_between(
            start_date=self._start, end_date=self._end
        )
