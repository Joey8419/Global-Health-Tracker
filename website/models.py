# Defines the database models
from global_health_tracker import db
from datetime import datetime
from flask_login import UserMixin


class Outbreak(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(255))
    iso2 = db.Column(db.String(2))
    iso3 = db.Column(db.String(3))
    year = db.Column(db.Integer)
    icd10n = db.Column(db.String(255))
    icd103n = db.Column(db.String(255))
    icd104n = db.Column(db.String(255))
    icd10c = db.Column(db.String(10))
    icd103c = db.Column(db.String(10))
    icd104c = db.Column(db.String(10))
    icd11c1 = db.Column(db.String(10))
    icd11c2 = db.Column(db.String(10))
    icd11c3 = db.Column(db.String(10))
    icd11l1 = db.Column(db.String(255))
    icd11l2 = db.Column(db.String(255))
    icd11l3 = db.Column(db.String(255))
    disease = db.Column(db.String(255))
    DONs = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())


# Each user can have multiple search entries with one-to-many relationships
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(150))
    searches = db.relationship('Search', backref='user', lazy=True)


class Search(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


