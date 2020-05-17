import os

from flask import Flask
from flask_restful import Api

from models.base import db
from resources.statistics import StatisticResource, StatisticResourceList


def create_app(conf):
    app = Flask(__name__)
    app.config.from_object(conf)

    db.init_app(app)
    with app.app_context():
        db.drop_all()
        db.create_all()

    api = Api(app, catch_all_404s=True)
    # mapping resource with routes
    api.add_resource(StatisticResource, '/v1/statistics/<int:statistic_id>')
    api.add_resource(StatisticResourceList, '/v1/statistics')

    return app


if __name__ == '__main__':
    app = create_app(os.environ.get(
        'CONFIG_ENVIRONMENT', 'conf.DevelopmentConfig'))
    app.run()
