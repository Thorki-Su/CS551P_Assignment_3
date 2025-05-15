from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    code = db.Column(db.String(10), nullable=False)
    region = db.Column(db.String(128))
    income_group = db.Column(db.String(128))

    data = db.relationship('EmissionData', backref='country', cascade="all, delete-orphan")

class EmissionData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    emission = db.Column(db.Float, nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)
