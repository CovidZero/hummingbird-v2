import os
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager


def setup_app():
    _app = Flask(__name__)
    _app.config.from_object(f"config.{os.environ['FLASK_ENV']}")
    return _app


def setup_jwt_auth(_app):
    return JWTManager(_app)


def setup_database(_app):
    _db = SQLAlchemy()
    _db.init_app(_app)
    return _db


def setup_database_migration(_app, _db):
    return Migrate(_app, _db)


app = setup_app()
jwt = setup_jwt_auth(app)
db = setup_database(app)
