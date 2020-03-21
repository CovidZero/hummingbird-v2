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


class DevelopmentConfig(DefaultConfig):
    ...


class TestingConfig(DefaultConfig):
    TESTING = True


class StagingConfig(DefaultConfig):
    TESTING = False


class ProductionConfig(DefaultConfig):
    TESTING = False
    DEBUG = False


default = DefaultConfig()
development = DevelopmentConfig()
testing = TestingConfig()
staging = StagingConfig()
production = ProductionConfig()
