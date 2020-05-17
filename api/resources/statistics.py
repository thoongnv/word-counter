import datetime

from flask_restful import Resource, abort, reqparse

from models.base import db
from models.sites import Site
from models.words import Word
from utils.counter import WordCounter

parser = reqparse.RequestParser()
parser.add_argument('website_url', type=str)


def abort_if_statistic_not_exist(
        statistic_id=False, website_url=False, raise_error=True):
    statistic = False
    if statistic_id:
        statistic = Site.query.get(statistic_id)

    if not statistic and website_url:
        statistic = Site.query.filter_by(url=website_url).first()

    if not statistic and raise_error:
        abort(404, message='Statistic does not exist')
    return statistic


class StatisticResource(Resource):
    def get(self, statistic_id):
        statistic = abort_if_statistic_not_exist(statistic_id)
        return statistic, 200

    def put(self, statistic_id):
        statistic = abort_if_statistic_not_exist(statistic_id)
        # recalculate statistic
        return {'id': statistic.id}, 200

    def delete(self, statistic_id):
        statistic = abort_if_statistic_not_exist(statistic_id)
        # remove statistic
        db.session.delete(statistic)
        db.session.commit()
        return {'id': None}, 200


class StatisticResourceList(Resource):
    def get(self):
        return [], 200

    def post(self):
        params = parser.parse_args()
        website_url = params.get('website_url', '')
        statistic = False
        if website_url:
            counter, error = WordCounter.from_website(website_url)
            if error:
                abort(400, message=error)

            statistic = abort_if_statistic_not_exist(
                website_url=website_url, raise_error=False)
            if not statistic:
                statistic = Site(url=website_url)
                db.session.add(statistic)
            else:
                # already have statistics, remove it
                delete_words_q = Word.__table__.delete().where(
                    Word.site_id == statistic.id)
                db.session.execute(delete_words_q)

            for word, frequency in counter.items():
                statistic.words.append(
                    Word(name=word, frequency=frequency))
            statistic.updated_at = datetime.datetime.now()
            db.session.commit()

        return {'id': statistic.id}, 201
