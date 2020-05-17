from models.base import db, to_json


class Site(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False, unique=True)
    updated_at = db.Column(db.DateTime())

    @property
    def json(self):
        return to_json(self, self.__class__)
