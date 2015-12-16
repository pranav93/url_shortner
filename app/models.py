from datetime import datetime
from app import db


class UrlInfo(db.Model):
    __tablename__ = 'url_info'
    id = db.Column(db.Integer, primary_key=True)
    url_hash = db.Column(db.String(64), index=True, unique=True)
    url = db.Column(db.String(128), index=True, unique=True)
    tiny_url = db.Column(db.String(128), unique=True)
    title = db.Column(db.String(32), index=True)

    def __repr__(self):
        return '<Url %r>' % self.url


class UrlHits(db.Model):
    __tablename__ = 'url_hits'
    id = db.Column(db.Integer, primary_key=True)
    url_hash = db.Column(db.String(64), db.ForeignKey('url_info.url_hash'))
    visit_time = db.Column(db.DateTime, default=datetime.utcnow)