from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
# moment = Moment(app)
# app.config.from_object('config')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ahmed:123@localhost:5432/fyyur'
db = SQLAlchemy()
migrate = Migrate(app, db)


class Venue(db.Model):
    __tablename__ = 'Venue'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String())
    facebook_link = db.Column(db.String())
    website = db.Column(db.String())
    seeking_talent = db.Column(db.String())
    seeking_description = db.Column(db.String())
    shows = db.relationship('Show', backref='venuee', lazy=True, cascade="save-update, merge, delete")

    def __repr__(self):
        return f'<Venue {self.id} {self.name} {self.city} {self.state} {self.address} {self.phone} {self.genres} {self.image_link} {self.facebook_link} {self.website} {self.seeking_talent} {self.seeking_description}>'

    # TODO: implement any missing fields, as a database migration using Flask-Migrate


class Artist(db.Model):
    __tablename__ = 'Artist'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String())
    facebook_link = db.Column(db.String())
    website = db.Column(db.String())
    seeking_talent = db.Column(db.String())
    seeking_description = db.Column(db.String())
    shows = db.relationship('Show', backref='artist', lazy=True, cascade="save-update, merge, delete")

    def __repr__(self):
        return f'<Artist {self.id} {self.name} {self.city} {self.state} {self.phone} {self.genres} {self.image_link} {self.facebook_link} {self.website} {self.seeking_talent} {self.seeking_description}>'


# Class Show has a relation (one-many) with two other tables
class Show(db.Model):
    __tablename__ = 'shows'
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime)
    venueeId = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    artistId = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)

    def __repr__(self):
        return f'<Show {self.id} {self.start_time} {self.venueeId} {self.artistId} >'
