
from app import db


class SomeModel(db.Model):
    __tablename__ = 'some_model'
    id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.Integer, nullable=False)

    def save(self, session, **kwargs):
        credential = SomeModel(
            name=kwargs['name']
        )
        session.add(credential)
        return credential
