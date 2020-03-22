
from app import db


class SomeModel(db.Model):
    __tablename__ = 'some_model'
    id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.Integer, nullable=False)

    def save(self, session, **kwargs):
        model = SomeModel(
            id=kwargs['id'],
            name=kwargs['name']
        )
        session.add(model)
        return model


# Model City -> Country(String), State(String), City(String),
# totalCases(Int), suspects(Int), refuses(Int), deaths(Int), recovered(Int)
class City(db.Model):
    __tablename__ = 'CITY'
    city = db.Column(db.String(255), primary_key=True)
    state = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    total_cases = db.Column(db.Integer)
    suspects = db.Column(db.Integer)
    refuses = db.Column(db.Integer)
    deaths = db.Column(db.Integer)
    recovered = db.Column(db.Integer)

    def save(self, session, **kwargs):
        model = City(**kwargs
                     )
        session.add(model)
        return model


# Model State -> Country(String), State(String),
# totalCases(Int), totalCasesMS(Int),
# notConfirmedByMS(Int), Deaths(Int), URL(String)
class State(db.Model):
    __tablename__ = 'STATE'
    state = db.Column(db.String(255), primary_key=True)
    country = db.Column(db.String(255), nullable=False)
    total_cases = db.Column(db.Integer)
    total_cases_ms = db.Column(db.Integer)
    not_confirmed_by_ms = db.Column(db.Integer)
    deaths = db.Column(db.Integer)
    url = db.Column(db.String(255), nullable=False)

    def save(self, session, **kwargs):
        model = State(**kwargs
                      )
        session.add(model)
        return model


# Model StatesPerDay -> Date(Date), Country(String),
# State(String), newCases(Int), totalCases(Int)
class StatesPerDay(db.Model):
    __tablename__ = 'STATES_PER_DAY'
    id = db.Column(db.String(255), primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    country = db.Column(db.String(255), primary_key=True)
    state = db.Column(db.String(255), nullable=False)
    new_cases = db.Column(db.Integer)
    total_cases = db.Column(db.Integer)

    def save(self, session, **kwargs):
        model = StatesPerDay(**kwargs
                             )
        session.add(model)
        return model


class TestPoint(db.Model):
    __tablename__ = 'TEST_POINT'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    zip_code = db.Column(db.String(255))
    latitude = db.Column(db.Float(asdecimal=True), nullable=False)
    longitude = db.Column(db.Float(asdecimal=True), nullable=False)

    def save(self, session, **kwargs):
        model = TestPoint(**kwargs)
        session.add(model)
        return model

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
           'id': self.id,
           'name': self.name,
           'address': self.address,
           'city': self.city,
           'zip_code': self.zip_code,
           'latitude': float(self.latitude),
           'longitude': float(self.longitude)
        }


# Model City -> Longitude(Float), Latitude(Float), Status(String)
class CasesLocation(db.Model):
    __tablename__ = 'CASES_LOCATION'
    id = db.Column(db.String(255), primary_key=True)
    city = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(255), nullable=False)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)

    def save(self, session, **kwargs):
        model = CasesLocation(**kwargs)
        session.add(model)
        return model
