import os
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_seeder import FlaskSeeder
from flask_cors import CORS


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


def setup_database_seeder(_app, _db):
    seeder = FlaskSeeder()
    seeder.init_app(_app, _db)


app = setup_app()
jwt = setup_jwt_auth(app)
db = setup_database(app)
CORS(app, resources={r"/data_api/v1/data/*": {"origins": "*"}})
