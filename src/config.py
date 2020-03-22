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
    SWAGGER_SUPPORTED_SUBMIT_METHODS = []
    RESTPLUS_MASK_HEADER = False
    RESTPLUS_MASK_SWAGGER = False

    # AUTHORIZATION
    AUTH_USERNAME = 'hummingbird'
    AUTH_PASSWORD = '477FABBF689B7'

    # JWT CONFIG
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'kECVeGbqnkGvAscsFreoH8SSUXdd7gve')
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    JWT_ACCESS_TOKEN_EXPIRES = 3600


class DevelopmentConfig(DefaultConfig):
    ...


class TestingConfig(DefaultConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test_data/test.db')


class StagingConfig(DefaultConfig):
    TESTING = False


class ProductionConfig(DefaultConfig):
    TESTING = False
    DEBUG = False

    # AUTHORIZATION
    # TODO: Create these credentials
    #AUTH_USERNAME = ''
    #AUTH_PASSWORD = ''

    # JWT CONFIG
    # TODO: Setup a secret key
    #JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', '')
    JWT_ACCESS_TOKEN_EXPIRES = 3600


default = DefaultConfig()
development = DevelopmentConfig()
testing = TestingConfig()
staging = StagingConfig()
production = ProductionConfig()
