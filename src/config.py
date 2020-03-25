import os
basedir = os.path.abspath(os.path.dirname(__file__))


class DefaultConfig(object):
    DEBUG = True
    TESTING = False
    BUNDLE_ERRORS = True
    PROPAGATE_EXCEPTIONS = True

    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Swagger
    RESTPLUS_MASK_HEADER = False
    RESTPLUS_MASK_SWAGGER = False

    # AUTHORIZATION
    AUTH_USERNAME = 'hummingbird'
    AUTH_PASSWORD = '477FABBF689B7'

    # JWT CONFIG
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY',
                               'kECVeGbqnkGvAscsFreoH8SSUXdd7gve')
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    JWT_ACCESS_TOKEN_EXPIRES = 3600


class DevelopmentConfig(DefaultConfig):
    TESTING = False
    DEBUG = False

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2:' \
                              '//teste:teste@db:5432/hummingbird-v2'


class TestingConfig(DefaultConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = \
        'sqlite:///'+os.path.join(basedir, 'test_data/test.db')


class StagingConfig(DefaultConfig):
    TESTING = False
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://" \
                              f"{os.getenv('DB_USERNAME')}:" \
                              f"{os.getenv('DB_PASSWD')}@" \
                              f"{os.getenv('DB_ENDPOINT')}:" \
                              f"5432/" \
                              f"{os.getenv('DB_NAME')}"


class ProductionConfig(DefaultConfig):
    TESTING = False
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://" \
                              f"{os.getenv('DB_USERNAME', 'teste')}:" \
                              f"{os.getenv('DB_PASSWD', 'teste')}@" \
                              f"{os.getenv('DB_ENDPOINT', '127.0.0.1')}:" \
                              f"{os.getenv('DB_PORT','5432')}/" \
                              f"{os.getenv('DB_NAME', 'hummingbird-v2')}"
    # SWAGGER
    SWAGGER_SUPPORTED_SUBMIT_METHODS = []

    # AUTHORIZATION
    AUTH_USERNAME = os.getenv('AUTH_USERNAME', 'hummingbird_p')
    AUTH_PASSWORD = os.getenv('AUTH_PASSWORD', '88FDD586EF3A7')

    # JWT CONFIG
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', '2wrsaheZd6DhsOqYKjy')
    JWT_ACCESS_TOKEN_EXPIRES = 3600


local = DefaultConfig()
development = DevelopmentConfig()
testing = TestingConfig()
staging = StagingConfig()
production = ProductionConfig()
