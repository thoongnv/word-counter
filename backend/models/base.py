import datetime

from flask_sqlalchemy import SQLAlchemy


def to_json(inst, cls):
    """
    Convert sqlalchemy record to json
    """
    d = {}
    for c in cls.__table__.columns:
        v = getattr(inst, c.name)
        if v is None:
            d[c.name] = ''
        else:
            # convert other types
            if isinstance(v, datetime.datetime):
                d[c.name] = v.isoformat()
            else:
                d[c.name] = v
    return d


db = SQLAlchemy()
