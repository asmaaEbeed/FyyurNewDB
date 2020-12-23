# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import (
    Flask,
    render_template,
    request,
    Response,
    flash,
    redirect,
    url_for
)
from flask_moment import Moment
# from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
# from flask_migrate import Migrate
import sys
from datetime import datetime
from models import app, db, Venue, Artist, Show
# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

# app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ahmed:123@localhost:5432/fyyur2'
db.init_app(app)
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
# TODO: connect to a local postgresql database

# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#


# class Venue(db.Model):
#     __tablename__ = 'Venue'
#     id = db.Column(db.Integer, primary_key=True, nullable=False)
#     name = db.Column(db.String, nullable=False)
#     city = db.Column(db.String(120), nullable=False)
#     state = db.Column(db.String(120), nullable=False)
#     address = db.Column(db.String(120))
#     phone = db.Column(db.String(120))
#     genres = db.Column(db.String(120))
#     image_link = db.Column(db.String(500))
#     facebook_link = db.Column(db.String(120))
#     shows = db.relationship('Show', backref='venuee', lazy=True, cascade="save-update, merge, delete")

#     def __repr__(self):
#         return f'<Venue {self.id} {self.name} {self.city} {self.state} {self.address} {self.phone} {self.genres} {self.image_link} {self.facebook_link}>'

#     # TODO: implement any missing fields, as a database migration using Flask-Migrate


# class Artist(db.Model):
#     __tablename__ = 'Artist'
#     id = db.Column(db.Integer, primary_key=True, nullable=False)
#     name = db.Column(db.String, nullable=False)
#     city = db.Column(db.String(120), nullable=False)
#     state = db.Column(db.String(120), nullable=False)
#     phone = db.Column(db.String(120))
#     genres = db.Column(db.String(120))
#     image_link = db.Column(db.String(500))
#     facebook_link = db.Column(db.String(120))
#     shows = db.relationship('Show', backref='artist', lazy=True, cascade="save-update, merge, delete")

#     def __repr__(self):
#         return f'<Artist {self.id} {self.name} {self.city} {self.state} {self.phone} {self.genres} {self.image_link} {self.facebook_link}>'


# # Class Show has a relation (one-many) with two other tables
# class Show(db.Model):
#     __tablename__ = 'shows'
#     id = db.Column(db.Integer, primary_key=True)
#     start_time = db.Column(db.DateTime)
#     venueeId = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
#     artistId = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)

#     def __repr__(self):
#         return f'<Show {self.id} {self.start_time} {self.venueeId} {self.artistId}>'

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

    # TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime

# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------
# Remain Small Point
@app.route('/venues')
def venues():
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    # data=[{
    #   "city": "San Francisco",
    #   "state": "CA",
    #   "venues": [{
    #     "id": 1,
    #     "name": "The Musical Hop",
    #     "num_upcoming_shows": 0,
    #   }, {
    #     "id": 3,
    #     "name": "Park Square Live Music & Coffee",
    #     "num_upcoming_shows": 1,
    #   }]
    # }, {
    #   "city": "New York",
    #   "state": "NY",
    #   "venues": [{
    #     "id": 2,
    #     "name": "The Dueling Pianos Bar",
    #     "num_upcoming_shows": 0,
    #   }]
    # }]
    data = []
    #Select All city, state (distinct) => [{city1, state1},{city1, state2}....]
    cities = db.session.query(Venue.city, Venue.state).distinct(Venue.city, Venue.state)
    print("kj")
    print(cities)
    #city = [{city1},{state1}] ... => city1 = city[0], state1 = city[1]
    for city in cities:
        num_upcoming_shows = 0
        # SELECT Venue.id, Venue.name FROM "Venue" WHERE Venue.city == city[0] AND Venue.state = state[1]
        # Get all city in same state
        venues_in_city = db.session.query(Venue.id, Venue.name).filter(Venue.city == city[0]).filter(Venue.state == city[1])
        # Loop in each city to get shows for each city
        for venuesInCity in venues_in_city:
            num_upcoming_shows_temp = 0
            # Here get all shows for one city
            venues_shows = db.session.query(Show).filter(Show.venueeId == venuesInCity[0])
            print(venues_shows)
            for show in venues_shows:
                if(show.start_time > datetime.now()):
                    num_upcoming_shows_temp += 1
            num_upcoming_shows = num_upcoming_shows_temp
        data.append({
            "city": city[0],
            "state": city[1],
            "venues": venues_in_city,
            "num_upcoming_shows": num_upcoming_shows
        })
        # data = [city, state, venues]
    return render_template('pages/venues.html', areas=data)

# Done
@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    # response={
    #   "count": 1,
    #   "data": [{
    #     "id": 2,
    #     "name": "The Dueling Pianos Bar",
    #     "num_upcoming_shows": 0,
    #   }]
    # }
    search_term = request.form.get('search_term', '')
    venues = db.session.query(Venue).filter(Venue.name.ilike('%' + search_term + '%')).all()
    data = []

    for venue in venues:
        num_upcoming_shows = 0
        shows = db.session.query(Show).filter(Show.venueeId == venue.id)
        for show in shows:
            if(show.start_time > datetime.now()):
                num_upcoming_shows += 1
        data.append({
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": num_upcoming_shows
        })
    response = {
        "count": len(venues),
        "data": data
    }
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

# Done
@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    # venue = db.session.query(Venue).filter(Venue.id == venue_id).one()
    # # shows upcoming, past
    # list_shows = db.session.query(Show).filter(Show.venueeId == venue_id)
    # past_shows = []
    # upcoming_shows = []

    # for show in list_shows:
    #     artist = db.session.query(Artist.name, Artist.image_link).filter(Artist.id == show.artistId).one()
    #     show_add = {
    #         "artist_id": show.artistId,
    #         "artist_name": artist.name,
    #         "artist_image_link": artist.image_link,
    #         "start_time": show.start_time.strftime('%m/%d/%Y')
    #         }

    #     if (show.start_time < datetime.now()):
    #         #print(past_shows, file=sys.stderr)
    #         past_shows.append(show_add)
    #     else:
    #         upcoming_shows.append(show_add)
    
    # Project Edit1 ===========> Solve with JOIN 
    venue = Venue.query.get(venue_id)
    shows_details = db.session.query(Show).join(Artist).filter(Show.venueeId==venue_id).all()
    # past_shows_details = db.session.query(Show).join(Artist).filter(Show.venueeId=venue_id).all()
    print(shows_details)
    past_shows = []
    upcoming_shows = []
    for show in shows_details:
        print(show)
        artistData = db.session.query(Artist).join(Show).filter(Artist.id==show.artistId).one()
        print(artistData)
        if (show.start_time <= datetime.now()):
            past_shows.append({
                "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                "artist_image_link": artistData.image_link,
                "artist_id": show.artistId,
                "artist_name": artistData.name
            })
        elif(show.start_time > datetime.now()):
            upcoming_shows.append({
                "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                "artist_image_link": artistData.image_link,
                "artist_id": show.artistId,
                "artist_name": artistData.name
            })
    data = {
      "id": venue.id,
      "name": venue.name,
      "city": venue.city,
      "state": venue.state,
      "address": venue.address,
      "genres": venue.genres[:-1][1:].replace("\"", '').split(','),
      "image_link": venue.image_link,
      "facebook_link": venue.facebook_link,
      "website": venue.website,
      "seeking_talent": venue.seeking_talent,
      "seeking_description": venue.seeking_description,
      "past_shows": past_shows,
      "upcoming_shows": upcoming_shows,
      "past_shows_count": len(past_shows),
      "upcoming_shows_count": len(upcoming_shows),
    }

    # data3 = {
    #   "id": 3,
    #   "name": "Park Square Live Music & Coffee",
    #   "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
    #   "address": "34 Whiskey Moore Ave",
    #   "city": "San Francisco",
    #   "state": "CA",
    #   "phone": "415-000-1234",
    #   "website": "https://www.parksquarelivemusicandcoffee.com",
    #   "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
    #   "seeking_talent": False,
    #   "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    #   "past_shows": [{
    #     "artist_id": 5,
    #     "artist_name": "Matt Quevedo",
    #     "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    #     "start_time": "2019-06-15T23:00:00.000Z"
    #   }],
    #   "upcoming_shows": [{
    #     "artist_id": 6,
    #     "artist_name": "The Wild Sax Band",
    #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    #     "start_time": "2035-04-01T20:00:00.000Z"
    #   }, {
    #     "artist_id": 6,
    #     "artist_name": "The Wild Sax Band",
    #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    #     "start_time": "2035-04-08T20:00:00.000Z"
    #   }, {
    #     "artist_id": 6,
    #     "artist_name": "The Wild Sax Band",
    #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    #     "start_time": "2035-04-15T20:00:00.000Z"
    #   }],
    #   "past_shows_count": 1,
    #   "upcoming_shows_count": 1,
    # }
    # data = list(filter(lambda d: d['id'] == venue_id, [ data3]))[0]
    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)

# Done
@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    form = VenueForm(request.form)
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    venue = Venue(
        name=form.name.data,
        city=form.city.data,
        state=form.state.data,
        address=form.address.data,
        phone=form.phone.data,
        genres=form.genres.data,
        image_link=form.image_link.data,
        facebook_link=form.facebook_link.data,
        website=form.website.data,
        seeking_talent=form.seeking_talent.data,
        seeking_description=form.seeking_description.data
    )
    try:
        db.session.add(venue)
        db.session.commit()
        # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except:
        # TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
        # change data.name to form[name]
        flash('Opps, Error Ocuure ' + request.form['name'] + ' couldnt add')
    finally:
        db.session.close()
    # TODO: on unsuccessful db insert, flash an error instead.
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')

# Done
@app.route('/venues/<venue_id>', methods=['POST'])  #change method from DELETE to POST
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    venue_id = request.form.get('venue_id')
    deleted_venue = Venue.query.get(venue_id)
    venueName = deleted_venue.name
    try:
        db.session.delete(deleted_venue)
        db.session.commit()
        flash('Venue ' + venueName + ' was successfully deleted!')
    except:
        db.session.rollback()
        flash('The Venue ' + venueName + ' could not be deleted.')
    finally:
        db.session.close()

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return redirect(url_for('index'))


#  Artists
#  ----------------------------------------------------------------
# Done
@app.route('/artists')
def artists():
    # TODO: replace with real data returned from querying the database
    # data=[{
    #   "id": 4,
    #   "name": "Guns N Petals",
    # }, {
    #   "id": 5,
    #   "name": "Matt Quevedo",
    # }, {
    #   "id": 6,
    #   "name": "The Wild Sax Band",
    # }]
    artists = db.session.query(Artist.id, Artist.name)
    data = []
    for artist in artists:
        data.append({
          "id": artist[0],
          "name": artist[1]
        })
    return render_template('pages/artists.html', artists=data)

# Done
@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    # response={
    #   "count": 1,
    #   "data": [{
    #     "id": 4,
    #     "name": "Guns N Petals",
    #     "num_upcoming_shows": 0,
    #   }]
    # }
    search_term = request.form.get('search_term', '')
    artists = db.session.query(Artist).filter(Artist.name.ilike('%' + search_term + '%')).all()
    data = []

    for artist in artists:
        num_upcoming_shows = 0
        shows = db.session.query(Show).filter(Show.artistId == artist.id)
        for show in shows:
            if(show.start_time > datetime.now()):
                num_upcoming_shows += 1
        data.append({
            "id": artist.id,
            "name": artist.name,
            "num_upcoming_shows": num_upcoming_shows
        })
    response = {
        "count": len(artists),
        "data": data
    }
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

# Done
@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    # artist = db.session.query(Artist).filter(Artist.id == artist_id).one()
    # list_shows = db.session.query(Show).filter(Show.artistId == artist_id)
    # past_shows = []
    # upcoming_shows = []

    # for show in list_shows:
    #     venue = db.session.query(Venue.name, Venue.image_link).filter(Venue.id == show.venueeId).one()

    #     show_add = {
    #         "venue_id": show.venueeId,
    #         "venue_name": venue.name,
    #         "venue_image_link": venue.image_link,
    #         "start_time": show.start_time.strftime('%m/%d/%Y')
    #         }

    #     if (show.start_time < datetime.now()):
    #         #print(past_shows, file=sys.stderr)
    #         past_shows.append(show_add)
    #     else:
    #         print(show_add, file=sys.stderr)
    #         upcoming_shows.append(show_add)

    artist = Artist.query.get(artist_id)
    shows_details = db.session.query(Show).join(Venue).filter(Show.artistId==artist_id).all()
    # past_shows_details = db.session.query(Show).join(Artist).filter(Show.venueeId=venue_id).all()
    print("jjjjjjjjjjj")
    print(shows_details)
    past_shows = []
    upcoming_shows = []
    for show in shows_details:
        print(show)
        venueData = db.session.query(Venue).join(Show).filter(Venue.id == show.venueeId).one()
        print("vvvvvvvvvvvvvvvv")
        print(venueData)
        if (show.start_time <= datetime.now()):
            past_shows.append({
                "start_time": show.start_time.strftime('%m/%d/%Y'),
                "venue_image_link": venueData.image_link,
                "venue_id": show.venueeId,
                "venue_name": venueData.name
            })
        elif(show.start_time > datetime.now()):
            upcoming_shows.append({
                "start_time": show.start_time.strftime('%m/%d/%Y'),
                "venue_image_link": venueData.image_link,
                "venue_id": show.artistId,
                "venue_name": venueData.name
            })
    data = {
        "id": artist.id,
        "name": artist.name,
        "city": artist.city,
        "state": artist.state,
        "genres": artist.genres[:-1][1:].replace("\"", '').split(','),
        "image_link": artist.image_link,
        "facebook_link": artist.facebook_link,
        "website": artist.website,
        "seeking_talent": artist.seeking_talent,
        "seeking_description": artist.seeking_description,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }
    # data1={
    #   "id": 4,
    #   "name": "Guns N Petals",
    #   "genres": ["Rock n Roll"],
    #   "city": "San Francisco",
    #   "state": "CA",
    #   "phone": "326-123-5000",
    #   "website": "https://www.gunsnpetalsband.com",
    #   "facebook_link": "https://www.facebook.com/GunsNPetals",
    #   "seeking_venue": True,
    #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    #   "past_shows": [{
    #     "venue_id": 1,
    #     "venue_name": "The Musical Hop",
    #     "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    #     "start_time": "2019-05-21T21:30:00.000Z"
    #   }],
    #   "upcoming_shows": [],
    #   "past_shows_count": 1,
    #   "upcoming_shows_count": 0,
    # }

    # data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
    return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
# Not Done1 ===>Done
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist_data = db.session.query(Artist).filter(Artist.id == artist_id).one()
    artist = {
        "name": artist_data.name,
        "city": artist_data.city,
        "state": artist_data.state,
        "phone": artist_data.phone,
        "genres": artist_data.genres.split(','),
        "image_link": artist_data.image_link,
        "facebook_link": artist_data.facebook_link,
        "website": artist_data.website,
        "seeking_talent": artist_data.seeking_talent,
        "seeking_description": artist_data.seeking_description,

    }
    # artist={
    #   "id": 4,
    #   "name": "Guns N Petals",
    #   "genres": ["Rock n Roll"],
    #   "city": "San Francisco",
    #   "state": "CA",
    #   "phone": "326-123-5000",
    #   "website": "https://www.gunsnpetalsband.com",
    #   "facebook_link": "https://www.facebook.com/GunsNPetals",
    #   "seeking_venue": True,
    #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
    # }
        
    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)


# Not Done2 ==> done
@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    artist = Artist.query.get(artist_id)
    artist.name = request.form['name']
    artist.city = request.form['city']
    artist.state = request.form['state']
    artist.phone = request.form['phone']
    artist.facebook_link = request.form['facebook_link']
    artist.genres = request.form.getlist('genres')
    artist.website = request.form['website']
    artist.seeking_talent = request.form['seeking_talent']
    artist.seeking_description = request.form['seeking_description']
    try:
        db.session.commit()
        flash("Artist " + artist.name + " is updated successfully")
    except:
        db.session.rollback()
        flash("Artist " + artist.name + " isn't updated successfully")
    finally:
        db.session.close()
    return redirect(url_for('show_artist', artist_id=artist_id))


# Not Done3 ==> done
@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue_data = db.session.query(Venue).filter(Venue.id == venue_id).one()
    venue = {
        "name": venue_data.name,
        "city": venue_data.city,
        "state": venue_data.state,
        "address": venue_data.address,
        "phone": venue_data.phone,
        "genres": venue_data.genres.split(','),
        "image_link": venue_data.image_link,
        "facebook_link": venue_data.facebook_link

    }
    # venue={
    #     "id": 1,
    #     "name": "The Musical Hop",
    #     "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    #     "address": "1015 Folsom Street",
    #     "city": "San Francisco",
    #     "state": "CA",
    #     "phone": "123-123-1234",
    #     "website": "https://www.themusicalhop.com",
    #     "facebook_link": "https://www.facebook.com/TheMusicalHop",
    #     "seeking_talent": True,
    #     "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    #     "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
    # }
    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)

# Not Done4 ==> done
@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    venue = Venue.query.get(venue_id)
    venue.name = request.form['name']
    venue.city = request.form['city']
    venue.state = request.form['state']
    venue.address = request.form['address']
    venue.phone = request.form['phone']
    venue.facebook_link = request.form['facebook_link']
    # venue.genres = request.form['genres'].split(',')
    venue.genres = request.form.getlist('genres')
    venue.website = request.form['website']
    venue.seeking_talent = request.form['seeking_talent']
    venue.seeking_description = request.form['seeking_description']
    try:
        db.session.commit()
        flash("Venue " + venue.name + " is updated successfully")
    except:
        db.session.rollback()
        flash("venue " + venue.name + " isn't updated successfully")
    finally:
        db.session.close()
    return redirect(url_for('show_venue', venue_id=venue_id))
    # # TODO: take values from the form submitted, and update existing
    # # venue record with ID <venue_id> using the new attributes
    # return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

# Done
@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)

#Done
@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    form = ArtistForm(request.form)
    # TODO: insert form data as a new Artist record in the db, instead
    artist = Artist(
        name=form.name.data,
        city=form.city.data,
        state=form.state.data,
        phone=form.phone.data,
        genres=form.genres.data,
        image_link=form.image_link.data,
        facebook_link=form.facebook_link.data,
        website=form.website.data,
        seeking_talent=form.seeking_talent.data,
        seeking_description=form.seeking_description.data,

    )
    # TODO: modify data to be the data object returned from db insertion
    try:
        db.session.add(artist)
        db.session.commit()
        # on successful db insert, flash success
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except:
        # TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
        # change data.name to form[name]
        db.session.rollback()
        flash('Opps, Error Occure ' + request.form['name'] + ' couldnt add')
    finally:
        db.session.close()
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

#Done
@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    data = []
    shows = db.session.query(Show.artistId, Show.venueeId, Show.start_time).all()
    print(shows)
    for show in shows:
        artist = db.session.query(Artist.name, Artist.image_link).filter(Artist.id == show[0]).one()
        venue = db.session.query(Venue.name).filter(Venue.id == show[1]).one()
        data.append({
            "venue_id": show[1],
            "venue_name": venue[0],
            "artist_id": show[0],
            "artist_name": artist[0],
            "artist_image_link": artist[1],
            "start_time": str(show[2])
        })
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    form = ShowForm(request.form)
    # TODO: insert form data as a new Show record in the db, instead
    show = Show(
        start_time=form.start_time.data,
        venueeId=form.venueeId.data,
        artistId=form.artistId.data
    )
    # on successful db insert, flash success
    try:
        db.session.add(show)
        db.session.commit()
        flash('Show was successfully listed!')
    except:
        db.session.rollback()
        # TODO: on unsuccessful db insert, flash an error instead.
        flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    finally:
        db.session.close()
    return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
