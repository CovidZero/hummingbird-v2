import os
basedir = os.path.abspath(os.path.dirname(__file__))


class DefaultConfig(object):
    DEBUG = True
    TESTING = False
    BUNDLE_ERRORS = True
    PROPAGATE_EXCEPTIONS = True


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
