from models.base import db, to_json


class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    frequency = db.Column(db.Integer)
    site_id = db.Column(db.Integer, db.ForeignKey('site.id'), nullable=False)
    site = db.relationship(
        'Site',
        backref=db.backref('words', lazy='dynamic', cascade='all, delete'))

    @property
    def json(self):
        return to_json(self, self.__class__)
