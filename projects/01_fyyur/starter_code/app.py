#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from flask_migrate import Migrate
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
import sys
import collections
import collections.abc
collections.Callable = collections.abc.Callable


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

migrate = Migrate(app, db)

# (Hecho) TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column((db.String(120)))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    looking_talent= db.Column(db.Boolean)
    description = db.Column(db.String(120))
    
  

    # (hecho) TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column((db.String(120)))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    looking_venues = db.Column(db.Boolean)
    description = db.Column(db.String(120))
    

    # (Hecho) TODO: implement any missing fields, as a database migration using Flask-Migrate

class Show(db.Model):
  __tablename__='Show'
  id = db.Column(db.Integer, primary_key=True)
  show_date = db.Column(db.Date, nullable=False)

  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False) 
 
  artist = db.relationship(Artist, backref=db.backref('shows', cascade='all, delete'))
  venue = db.relationship(Venue, backref=db.backref('shows', cascade='all, delete'))
  

# (Hecho) TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # (hecho) TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  locals = []
  all_places = Venue.query.distinct(Venue.city, Venue.state).all()
  for place in all_places:
        local = {
            'city': place.city,
            'state': place.state
        }
        locals.append(local)
  venues = Venue.query.all()
  for local in locals:
        local["venues"] = []
        for venue in venues:
            if venue.city == local["city"] and venue.state == local["state"]:
                v = {
                    'id': venue.id,
                    'name': venue.name
                }
                local["venues"].append(v)
  return render_template('pages/venues.html', areas=locals)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  response={
    "count": 1,
    "data": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  
  # shows the venue page with the given venue_id
  # (Hecho) TODO: replace with real venue data from the venues table, using venue_id

 
  data = Venue.query.filter_by(id = venue_id).first()
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  error = False
  form = VenueForm()
  try: 
    name = form.name.data
    city = form.city.data
    state = form.state.data
    address = form.address.data
    phone = form.phone.data
    genres = form.genres.data
    image_link = form.image_link.data
    facebook_link = form.facebook_link.data
    website_link = form.website_link.data
    looking_talent= form.seeking_talent.data
    description = form.seeking_description.data

    venue = Venue(name = name, city = city, state = state, address = address, phone = phone, genres = genres, image_link = image_link, facebook_link = facebook_link, 
    website_link = website_link, looking_talent = looking_talent, description = description)
    
    db.session.add(venue)
    db.session.commit()
  
  except:
    db.session.rollback()
    error = True
    print(sys.exec_info())
  finally:
    db.session.close()

  # (Hecho) TODO: insert form data as a new Venue record in the db, instead
  # (hecho) TODO: modify data to be the data object returned from db insertion
  
  if error:
    abort(500)
    flash('An error occurred. Venue ' + name + ' could not be listad.')
  else:
    flash('Venue ' + form.name.data + ' was successfully listed!')

  
  # (Hecho) TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  data = Artist.query.all()
 
 # (Hecho) TODO: replace with real data returned from querying the database
 
  print (data)
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  response={
    "count": 1,
    "data": [{
      "id": 4,
      "name": "Guns N Petals",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # (Hecho) TODO: replace with real artist data from the artist table, using artist_id

  data = Artist.query.filter_by(id = artist_id).first()
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.filter_by(id = artist_id).first()

  form.name.data = artist.name
  form.city.data = artist.city
  form.state.data = artist.state
  form.phone.data = artist.phone
  form.genres.data = artist.genres
  form.image_link.data = artist.image_link
  form.facebook_link.data = artist.facebook_link
  form.website_link.data = artist.website_link
  form.seeking_venue.data = artist.looking_venues
  form.seeking_description.data = artist.description

  print(artist.name)
 
  # (hecho) TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  error = False
  form = ArtistForm()
  try:
    
    name = form.name.data
    city = form.city.data
    state = form.state.data
    phone = form.phone.data
    genres = form.genres.data
    facebook_link = form.facebook_link.data
    website = form.website_link.data
    looking_venues= form.seeking_venue.data
    description = form.seeking_description.data

    artist = Artist(name = name, city = city, state = state, phone = phone, genres = genres, facebook_link = facebook_link, 
  website_link = website, looking_venues = looking_venues, description = description)

    db.session.add(artist)
    db.session.commit()

  except:
    db.session.rollback()
    error = True
    print(sys.exec_info())

  finally:
      db.session.close()

  if error:
    abort(500)
    flash('An error occurred. Artist ' + name + ' could not be updated.')
  else:
    flash('Artist ' + name + ' was successfully updated!')
  
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()

  venue = Venue.query.filter_by(id = venue_id).first()

  form.name.data = venue.name
  form.city.data = venue.city
  form.state.data = venue.state
  form.address.data = venue.address
  form.phone.data = venue.phone
  form.genres.data = venue.genres
  form.image_link.data = venue.image_link
  form.facebook_link.data = venue.facebook_link
  form.website_link.data = venue.website_link
  form.seeking_talent.data = venue.looking_talent
  form.seeking_description.data = venue.description

  # (Hecho) TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():

  error = False
  form = ArtistForm()
  try: 
    name = form.name.data
    city = form.city.data
    state = form.state.data
    phone = form.phone.data
    genres = form.genres.data
    image_link = form.image_link.data
    facebook_link = form.facebook_link.data
    website_link = form.website_link.data
    looking_venues= form.seeking_venue.data
    description = form.seeking_description.data

    artist = Artist(name = name, city = city, state = state, phone = phone, genres = genres, image_link = image_link, facebook_link = facebook_link, 
    website_link = website_link, looking_venues = looking_venues, description = description)
    
    db.session.add(artist)
    db.session.commit()
  
  except:
    db.session.rollback()
    error = True
    print(sys.exec_info())
  
  finally:
    db.session.close()


  # called upon submitting the new artist listing form
  # (Hecho) TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  if error:
    abort(500)
    flash('An error occurred. Artist ' + name + ' could not be listed.')
  else:
    flash('Artist ' + form.name.data + ' was successfully listed!')
  # on successful db insert, flash success
  #flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # (Hecho) TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # (hecho) TODO: replace with real venues data.

  todo_shows = Show.query.join(Artist, Venue).all()
  print(todo_shows)

  return render_template('pages/shows.html', shows=todo_shows)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # (Hecho) TODO: insert form data as a new Show record in the db, instead
  
  error = False
  form = ShowForm()
  try: 
    artist_id = form.artist_id.data
    venue_id = form.venue_id.data
    show_date= form.start_time.data

    show = Show(artist_id = artist_id, venue_id = venue_id, show_date = show_date)
    
    db.session.add(show)
    db.session.commit()
  
  except:
    db.session.rollback()
    error = True
    print(sys.exec_info())
  finally:
    db.session.close()

  if error:
      abort(500)
      flash('An error occurred. Show could not be created.')
  else:
      flash('Show was successfully listed!')
    # (Hecho) TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

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
