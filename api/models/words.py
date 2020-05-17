from models.base import db


class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    frequency = db.Column(db.Integer)
    site_id = db.Column(db.Integer, db.ForeignKey('site.id'), nullable=False)
    site = db.relationship('Site', backref=db.backref('words', lazy=True))
