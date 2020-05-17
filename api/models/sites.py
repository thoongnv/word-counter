from models.base import db


class Site(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False, unique=True)
    updated_at = db.Column(db.DateTime())
