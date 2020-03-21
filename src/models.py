
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
