from app import db
from sqlalchemy.orm import relationship


class City(db.Model):
    __tablename__ = 'casespercity'
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(255))
    city = db.Column(db.String(255), primary_key=True)
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'))
    totalcases = db.Column(db.Integer)
    state_data = relationship("State")

    def save(self, session, **kwargs):
        model = City(**kwargs)
        session.add(model)
        return model

    @property
    def active_cases(self):
        return (self.totalcases)


class State(db.Model):
    __tablename__ = 'state'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    abbreviation = db.Column(db.String)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)

    def save(self, session, **kwargs):
        model = State(**kwargs)
        session.add(model)
        return model


class StateCases(db.Model):
    __tablename__ = 'casesperstate'
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String)
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'))
    totalcases = db.Column(db.Integer)
    totalcasesms = db.Column(db.Integer)
    notconfirmedbyms = db.Column(db.Integer)
    deaths = db.Column(db.Integer)
    url = db.Column(db.String)
    state_data = relationship("State")

    def save(self, session, **kwargs):
        model = StateCases(**kwargs)
        session.add(model)
        return model

    def fetch_all(self, session):
        return session.query(self.__class__).all()


class StatesPerDay(db.Model):
    __tablename__ = 'casesstateperday'
    id = db.Column(db.String(255), primary_key=True)
    date = db.Column(db.Date)
    country = db.Column(db.String(255))
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'))
    newcases = db.Column(db.Integer)
    totalcases = db.Column(db.Integer)
    state_data = relationship("State")

    def save(self, session, **kwargs):
        model = StatesPerDay(**kwargs)
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
