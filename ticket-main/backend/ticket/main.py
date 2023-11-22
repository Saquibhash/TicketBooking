from datetime import date, datetime, timedelta
import dateutil.tz
import sqlite3
from flask import Blueprint, abort, render_template, request, flash, url_for, redirect, Response, send_file, current_app, make_response 
from flask_jwt_extended import get_jwt_identity, jwt_required
import flask_login
from flask_login import current_user 
from sqlalchemy import func
from io import BytesIO
import tempfile
import json
from .manager import compute_reserved_seats
from .model import Movie, Venue, shw, User, booking
from .schema import movie_schema, showtime_schema, venue_schema,user_schema
from flask import jsonify
from .db import db as db_instance
from . import model
from .tasks import export_venue_csv 
import csv
import io
from .cache import cache


db = db_instance.database

blue = Blueprint("main", __name__)

@blue.route("/")
@cache.cached(timeout=60)
def index():
    current_day = date.today()
    future = current_day + timedelta(days=7)

    # Assuming 'shw' is a model with fields that can be serialized to JSON
    next_shows = shw.query.filter(shw.day > current_day, shw.day <= future).order_by(shw.day.asc(), shw.time.asc()).all()
    today_shows = shw.query.filter(shw.day == current_day).order_by(shw.time.asc()).all()

    # Serialize the show data using Marshmallow schema, including movie details
    serialized_next_shows = [showtime_schema.dump(show) for show in next_shows]
    serialized_today_shows = [showtime_schema.dump(show) for show in today_shows]
    movies = Movie.query.all()
    serialized_movies = [movie_schema.dump(movie) for movie in movies]
    venues = Venue.query.all()
    serialized_venues = [venue_schema.dump(venue) for venue in venues]

    # Include movie and venue details for "next show"
    for show in serialized_next_shows:
        movie_id = show["movie_id"]
        venue_id = show["venue_id"]
        movie = next((movie for movie in serialized_movies if movie["id"] == movie_id), None)
        venue = next((venue for venue in serialized_venues if venue["id"] == venue_id), None)
        if movie:
            show["movie"] = movie
        if venue:
            show["venue"] = venue
            # Add seat booked and seat available information
            num_seats_booked = venue["num_total_seats"] - compute_reserved_seats(show["id"])
            show["seats_booked"] = num_seats_booked
            show["seats_available"] = venue["num_total_seats"] - num_seats_booked

    # Include movie and venue details for "current show" (today's show)
    for show in serialized_today_shows:
        movie_id = show["movie_id"]
        venue_id = show["venue_id"]
        movie = next((movie for movie in serialized_movies if movie["id"] == movie_id), None)
        venue = next((venue for venue in serialized_venues if venue["id"] == venue_id), None)
        if movie:
            show["movie"] = movie
        if venue:
            show["venue"] = venue
            # Add seat booked and seat available information
            num_seats_booked = venue["num_total_seats"] - compute_reserved_seats(show["id"])
            show["seats_booked"] = num_seats_booked
            show["seats_available"] = venue["num_total_seats"] - num_seats_booked

    # Create a dictionary to hold all the data
    data = {
        "all_movies": serialized_movies,
        "next_shws": serialized_next_shows,
        "today_shws": serialized_today_shows,
        "venues": serialized_venues
    }

    return jsonify(data)




@blue.route("/movie/<int:id>", methods=["GET"])
@cache.cached(timeout=60)
def get_movie(id):
    movie = Movie.query.get(id)
    if not movie:
        abort(404)  # Return a 404 error if movie is not found

    current_day = date.today()
    shws = shw.query.filter(shw.movie_id == id, shw.day >= current_day).order_by(shw.day.asc(), shw.time.asc()).all()

    # Serialize the data
    movie_data = {
        "id": movie.id,
        "title": movie.title,
        "director": movie.director,
        "duration": movie.duration,
        "cast": movie.cast,
        "rating": movie.rating,
        "price": movie.price,
        "img": movie.img,
    }

    showtimes_data = []
    for show in shws:
        showtime_data = {
            "id": show.id,
            "day": show.day,
            "time": show.time.strftime("%H:%M"),  # Convert time to string representation
            "movie_id": show.movie_id,
            "venue_id": show.venue_id,
        }
        showtimes_data.append(showtime_data)

    response_data = {
        "movie": movie_data,
        "showtimes": showtimes_data,
    }

    return jsonify(response_data), 200

@blue.route("/venue/<int:id>", methods=["GET"])
@cache.cached(timeout=60)
def get_venue(id):
    venue = Venue.query.get(id)
    if not venue:
        abort(404) 

    venue_data = {
        "id": venue.id,
        "name": venue.name,
        "location": venue.location,
        "num_total_seats": venue.num_total_seats,
    }

    response_data = {
        "venue": venue_data,
    }

    return jsonify(response_data), 200

@blue.route("/show/<int:id>", methods=["GET"])
@cache.cached(timeout=60)
def get_show(id):
    show = shw.query.get(id)

    if not show:
        return jsonify({"message": "Show not found"}), 404

    serialized_show = showtime_schema.dump(show)

    movie = Movie.query.get(show.movie_id)
    venue = Venue.query.get(show.venue_id)

    if movie:
        serialized_show["movie"] = movie_schema.dump(movie)
    if venue:
        serialized_show["venue"] = venue_schema.dump(venue)

        num_seats_booked = venue.num_total_seats - compute_reserved_seats(show.id)
        serialized_show["seats_booked"] = num_seats_booked
        serialized_show["seats_available"] = venue.num_total_seats - num_seats_booked

    response_data = {
        "show": serialized_show,
    }

    return jsonify(response_data), 200

@blue.route("/user")
@jwt_required()
def user():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    serialized_user = user_schema.dump(user)

    current_day = date.today()
    now = []
    past = []
    now_bookings = model.booking.query.filter(model.booking.user_id == current_user_id).order_by(model.booking.date_time).all()
    
    for res in now_bookings:
        # Get the related movie, show, and venue information for each booking
        movie = res.shw.movie
        show = res.shw
        venue = res.shw.venue

        # Check if both movie, show, and venue objects exist and have their 'id' attributes
        if movie and hasattr(movie, 'id') and show and hasattr(show, 'id') and venue and hasattr(venue, 'id'):
            booking_info = {
                "id": res.id,
                "user_id": res.user_id,
                "show_id": res.shw_id,
                "num_seats": res.num_seats,
                "date_time": res.date_time.strftime("%Y-%m-%d %H:%M:%S"),
                "movie": {
                    "id": movie.id,
                    "title": movie.title,
                    "img": movie.img,
                    # Include any other movie details you need
                },
                "show": {
                    "id": show.id,
                    "day": show.day.strftime("%Y-%m-%d"),
                    "time": show.time.strftime("%H:%M:%S"),
                    # Include any other show details you need
                },
                "venue": {
                    "id": venue.id,
                    "name": venue.name,
                    "location": venue.location,
                    # Include any other venue details you need
                }
            }
            if res.shw.day >= current_day:
                now.append(booking_info)
            else:
                past.append(booking_info)
        else:
            # Handle the case where either the movie, show, or venue is not found or doesn't have an 'id' attribute
            # You can choose to skip the booking or add some default values in this case
            # For example, you can add a default venue name and location:
            booking_info = {
                "id": res.id,
                "user_id": res.user_id,
                "show_id": res.shw_id,
                "num_seats": res.num_seats,
                "date_time": res.date_time.strftime("%Y-%m-%d %H:%M:%S"),
                "movie": {
                    "id": movie.id if movie and hasattr(movie, 'id') else None,
                    "title": movie.title if movie else "Movie Not Found",
                    "img": movie.img if movie else "default_movie_img_url",
                    # Include any other movie details you need
                },
                "show": {
                    "id": show.id if show and hasattr(show, 'id') else None,
                    "day": show.day.strftime("%Y-%m-%d") if show else "Unknown Date",
                    "time": show.time.strftime("%H:%M:%S") if show else "Unknown Time",
                    # Include any other show details you need
                },
                "venue": {
                    "id": venue.id if venue and hasattr(venue, 'id') else None,
                    "name": venue.name if venue else "Venue Not Found",
                    "location": venue.location if venue else "Unknown Location",
                    # Include any other venue details you need
                }
            }
            if res.shw.day >= current_day:
                now.append(booking_info)
            else:
                past.append(booking_info)

    return jsonify(user=serialized_user,  now_bookings=now, past_bookings=past)


@blue.route("/booking/", defaults={'id': None})
@blue.route("/booking/<int:id>")
@jwt_required()
def booking(id):
    current_day = date.today()
    all_shws = shw.query.filter(shw.day >= current_day).order_by(shw.day.asc(), shw.time.asc()).all()
    
    if id is None:
        shws_data = []
        for shw in all_shws:
            shw_data = {
                "id": shw.id,
                "movie_id": shw.movie_id,
                "venue_id": shw.venue_id,
                "day": shw.day.strftime("%Y-%m-%d"),
                "time": shw.time.strftime("%H:%M:%S"),
            }
            shws_data.append(shw_data)
    else:
        shw = shw.query.get(id)        
        shws_data = {
            "id": shw.id,
            "movie_id": shw.movie_id,
            "venue_id": shw.venue_id,
            "day": shw.day.strftime("%Y-%m-%d"),
            "time": shw.time.strftime("%H:%M:%S"),
        }

    return jsonify(shws=shws_data)


@blue.route("/booking/", methods=["POST"])
@jwt_required()
def booking_post():
    data = request.get_json()
    current_user_id = get_jwt_identity()

    choosen_shw = data.get("shw")
    choosen_num_seats = data.get("seats")

    show = shw.query.get(choosen_shw)

    print(show.id, current_user_id, choosen_num_seats, datetime.now())
    new_booking = model.booking(shw_id=show.id,user_id=current_user_id,num_seats=int(choosen_num_seats),date_time=datetime.now())

    db.session.add(new_booking)
    db.session.commit()

    # Create a dictionary for the newly created booking
    booking_data = {
        "id": new_booking.id,
        "user_id": new_booking.user_id,
        "shw_id": new_booking.shw_id,
        "num_seats": new_booking.num_seats,
        "date_time": new_booking.date_time.strftime("%Y-%m-%d %H:%M:%S"),
    }

    # Return the booking data as a JSON response
    return jsonify(booking=booking_data)


@blue.route('/search')
@cache.cached(timeout=60)
def search():
    query = request.args.get('query', '')
    movies = Movie.query.filter((Movie.title.like(f'%{query.lower()}%')) | (Movie.rating == query)).all()
    venues = Venue.query.filter(func.lower(Venue.location).like(f'%{query}%')).all()

    print("Movies:", movies)  # Print movies for debugging
    print("Venues:", venues)  # Print venues for debugging


    # Create lists of movie and venue data
    movie_data = [
        {
            "id": movie.id,
            "title": movie.title,
            "rating": movie.rating,
            "img":movie.img
            # Add more fields as needed
        }
        for movie in movies
    ]

    venue_data = [
        {
            "id": venue.id,
            "name": venue.name,
            "location": venue.location,
            # Add more fields as needed
        }
        for venue in venues
    ]

    # Create a dictionary for the search results
    search_results = {
        "query": query,
        "movies": movie_data,
        "venues": venue_data,
    }

    # Return the search results as a JSON response
    return jsonify(search_results)

# Import necessary modules
import io
import csv
from flask import make_response, jsonify


@blue.route("/export_venue_csv/<int:id>")
@cache.cached(timeout=60)
def export_venue_csv(id):
    try:
        # Fetch the data for the selected venue based on the venue ID
        venue = Venue.query.get(id)

        if venue is None:
            return jsonify({'status': 'error', 'message': 'Venue not found'}), 404

        # Generate the CSV data for the selected venue and its shows
        output = io.StringIO()
        csv_writer = csv.writer(output)

        # Write venue details as header
        venue_headers = ['Venue Name', 'Location', 'Capacity']
        venue_data = [venue.name, venue.location, venue.num_total_seats]
        csv_writer.writerow(venue_headers)
        csv_writer.writerow(venue_data)

        # Fetch and add show details
        show_headers = ['Show Date', 'Show Time', 'Movie']
        csv_writer.writerow(show_headers)

        for show in venue.showed:
            show_data = [show.day.strftime('%Y-%m-%d'), show.time.strftime('%H:%M:%S'), show.movie.title]
            csv_writer.writerow(show_data)

        # Create a response with the CSV data
        csv_filename = f'venue_{venue.id}_data.csv'
        response = make_response(output.getvalue())
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = f'attachment; filename={csv_filename}'

        return response

    except Exception as e:
        error = {"error": str(e)}
        return jsonify(error)
