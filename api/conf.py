class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'cV0EQPlDaBTpRzDIcS35UA'
    SQLALCHEMY_DATABASE_URI = 'sqlite://../db.sqlite'


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'zKAA664G46LFlppb9Lb9Tg'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///word_counter.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'nXsA8NuWawH2QixdsqRiGQ'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///word_counter_test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
