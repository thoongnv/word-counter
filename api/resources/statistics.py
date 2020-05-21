import datetime
import logging

from flask.logging import default_handler
from flask_restful import Resource, abort, reqparse

from models.base import db
from models.sites import Site
from models.words import Word
from resources.base import get_paging_params
from utils.counter import WordCounter
from utils.misc import DEFAULT_PAGINATION_LIMIT

_logger = logging.getLogger()
_logger.addHandler(default_handler)

parser = reqparse.RequestParser()
parser.add_argument('website_url', type=str)
# paging fields
parser.add_argument('order', type=str)
parser.add_argument('offset', type=int, default=0)
parser.add_argument('limit', type=int, default=DEFAULT_PAGINATION_LIMIT)


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


def build_words(site, offset, limit, order_by):
    words = {
        'total': site.words.count(),
        'offset': offset,
        'limit': limit,
    }
    words['data'] = [word.json for word in site.words.order_by(order_by)[
        offset:offset + limit]]
    return words


class StatisticResource(Resource):
    def get(self, statistic_id):
        statistic = abort_if_statistic_not_exist(statistic_id)
        params = get_paging_params(parser.parse_args())
        offset = params['offset']
        limit = params['limit']
        order = params['order']
        order_by = None
        if 'frequency' in order:
            order_by = getattr(Word.frequency, order['frequency'])()

        parse_statistic = statistic.json
        parse_statistic['words'] = \
            build_words(statistic, offset, limit, order_by)
        return parse_statistic, 200

    def put(self, statistic_id):
        statistic = abort_if_statistic_not_exist(statistic_id)
        counter, error = WordCounter.from_website(statistic.url)
        if error:
            abort(400, message=error)

        # we actually need values to update but now just force recalculate
        # remmove current word counter
        delete_words_q = Word.__table__.delete().where(
            Word.site_id == statistic.id)
        db.session.execute(delete_words_q)

        # recalculate statistic
        for word, frequency in counter.items():
            statistic.words.append(Word(name=word, frequency=frequency))
        statistic.updated_at = datetime.datetime.now()
        db.session.commit()

        return {'id': statistic.id}, 200

    def delete(self, statistic_id):
        statistic = abort_if_statistic_not_exist(statistic_id)
        # remove statistic
        db.session.delete(statistic)
        db.session.commit()
        return {'id': None}, 200


class StatisticResourceList(Resource):
    def get(self):
        params = get_paging_params(parser.parse_args())
        offset = params['offset']
        limit = params['limit']
        order = params['order']
        sites = Site.query.offset(offset).limit(offset + limit).all()
        order_by = None
        if 'frequency' in order:
            order_by = getattr(Word.frequency, order['frequency'])()

        statistics = {
            'total': Site.query.count(),
            'offset': offset,
            'limit': limit,
            'data': []
        }
        for site in sites:
            parse_site = site.json
            parse_site['words'] = \
                build_words(site, 0, DEFAULT_PAGINATION_LIMIT, order_by)
            statistics['data'].append(parse_site)

        return statistics, 200

    def post(self):
        params = parser.parse_args()
        website_url = params.get('website_url', '')
        if website_url:
            counter, error = WordCounter.from_website(website_url)
            if error:
                abort(400, message=error)

            try:
                statistic = Site(url=website_url)
                db.session.add(statistic)
                for word, frequency in counter.items():
                    statistic.words.append(
                        Word(name=word, frequency=frequency))
                db.session.commit()
                return {'id': statistic.id}, 201
            except Exception as e:
                _logger.error(e)
                abort(400, message='Error occurred when count word frequency')

        abort(400, message='Missing website URL for word counting')
