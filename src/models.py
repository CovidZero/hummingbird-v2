from app import db
from sqlalchemy.orm import relationship
from sqlalchemy_pagination import paginate


class City(db.Model):
    __tablename__ = 'casespercity'
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(255))
    city = db.Column(db.String(255), primary_key=True)
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'))
    totalcases = db.Column(db.Integer)
    deaths = db.Column(db.Integer)
    ibge_id = db.Column(db.Integer)
    state_data = relationship("State")

    def save(self, session, **kwargs):
        model = City(**kwargs)
        session.add(model)
        return model

    @property
    def active_cases(self):
        return self.totalcases

    def fetch_all(self, session):
        return session.query(self.__class__).all()

    def fetch_paginated(self, session, page_number):
        query = session.query(self.__class__)
        paginator = paginate(query, int(page_number), 25)
        if int(page_number) > paginator.pages:
            return [], None
        pages_info = {
            'total_pages': paginator.pages,
            'has_next': paginator.has_next,
            'has_previous': paginator.has_previous,
            'next_page': paginator.next_page,
            'current_page': page_number,
        }
        return paginator.items, pages_info


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


class PredictCases(db.Model):
    __tablename__ = 'predictcases'
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String)
    date = db.Column(db.Date)
    predictcases = db.Column(db.Integer)
    update = db.Column(db.DateTime)

    def save(self, session, **kwargs):
        model = PredictCases(**kwargs)
        session.add(model)
        return model

    def fetch_all(self, session):
        return session.query(self.__class__).all()


class DataSus(db.Model):
    __tablename__ = 'datasus'
    id = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String)
    state = db.Column(db.String)
    coduf = db.Column(db.Integer)
    city = db.Column(db.String)
    date = db.Column(db.Date)
    newcases = db.Column(db.Integer)
    totalcases = db.Column(db.Integer)
    newdeaths = db.Column(db.Integer)
    totaldeaths = db.Column(db.Integer)
    update = db.Column(db.DateTime)
    codmun = db.Column(db.Integer)
    codhealthregion = db.Column(db.Integer)
    namehealthregion = db.Column(db.String)
    epiweek = db.Column(db.Integer)
    population = db.Column(db.Integer)
    recoverednew = db.Column(db.Integer)
    accompanyingnew = db.Column(db.Integer)

    def save(self, session, **kwargs):
        model = DataSus(**kwargs)
        session.add(model)
        return model

    def fetch_all(self, session):
        return session.query(self.__class__).all()

    def fetch_paginated(self, session, page_number):
        query = session.query(self.__class__)
        paginator = paginate(query, int(page_number), 25)
        if int(page_number) > paginator.pages:
            return [], None

        pages_info = {
            'total_pages': paginator.pages,
            'has_next': paginator.has_next,
            'has_previous': paginator.has_previous,
            'next_page': paginator.next_page,
            'current_page': page_number,
        }
        return paginator.items, pages_info


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

    def fetch_paginated(self, session, page_number):
        query = session.query(self.__class__)
        paginator = paginate(query, int(page_number), 25)
        if int(page_number) > paginator.pages:
            return [], None

        pages_info = {
            'total_pages': paginator.pages,
            'has_next': paginator.has_next,
            'has_previous': paginator.has_previous,
            'next_page': paginator.next_page,
            'current_page': page_number,
        }
        return paginator.items, pages_info


class StateCasesPerDay(db.Model):
    __tablename__ = 'casesstateperday'
    id = db.Column(db.String(255), primary_key=True)
    date = db.Column(db.Date)
    country = db.Column(db.String(255))
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'))
    newcases = db.Column(db.Integer)
    totalcases = db.Column(db.Integer)
    state_data = relationship("State")

    def save(self, session, **kwargs):
        model = StateCasesPerDay(**kwargs)
        session.add(model)
        return model

    def fetch_all(self, session):
        return session.query(self.__class__).all()

    def fetch_paginated(self, session, page_number):
        query = session.query(self.__class__)
        paginator = paginate(query, int(page_number), 25)
        if int(page_number) > paginator.pages:
            return [], None
        pages_info = {
            'total_pages': paginator.pages,
            'has_next': paginator.has_next,
            'has_previous': paginator.has_previous,
            'next_page': paginator.next_page,
            'current_page': page_number,
        }
        return paginator.items, pages_info


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
