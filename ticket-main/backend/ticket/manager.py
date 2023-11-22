from flask import request, redirect, url_for, render_template, Blueprint, flash
from flask_jwt_extended import get_jwt_identity, jwt_required, verify_jwt_in_request
import jwt

from .schema import movie_schema, venue_schema
from . import model
from datetime import date, timedelta
from functools import wraps
from datetime import datetime
from flask.json import jsonify
from .db import db as db_instance

db = db_instance.database




blue = Blueprint("manager", __name__)

def manager_only(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        if current_user_id is None:
            return jsonify({"message": "Unauthorized. User not authenticated."}), 401
        
        current_user = model.User.query.get(current_user_id)
        if current_user is None:
            return jsonify({"message": "Unauthorized. User not found."}), 401

        if current_user.role == model.UserRole.manager:
            return fn(*args, **kwargs)
        else:
            return jsonify({"message": "Unauthorized. Only managers are allowed."}), 403

    return wrapper


@blue.route("/validate")
def validate():
    try:
        verify_jwt_in_request()
        current_user_id = get_jwt_identity()
        user = model.User.query.get(current_user_id)
        
        if user and user.role ==  model.UserRole.manager:
            return {"status": True, "success": True, 'manager': True}, 200
        elif user and user.role == model.UserRole.customer:
            return {"status": True, "success": True, 'manager': False}, 200
        else:
            return {"status": False, "success": False, "message": "User is not authorized."}, 403
    
    except jwt.ExpiredSignatureError:
        return {"status": False, "success": False, "message": "JWT token has expired."}, 401
    except jwt.InvalidTokenError:
        return {"status": False, "success": False, "message": "Invalid JWT token."}, 401

@blue.route("/shows")
@jwt_required()
@manager_only
def shows():
    current_day = date.today()
    future = current_day + timedelta(days=7)
    past = current_day - timedelta(days=7)
    shws = model.shw.query.filter(model.shw.day <= future, model.shw.day >= past).order_by(model.shw.day.asc(), model.shw.time.asc()).all()
    num_results = []
    for sh in shws:
        if sh.venue is None:
            continue
        num_results.append(sh.venue.num_total_seats - compute_reserved_seats(sh.id))
    
    # Create a list of dictionaries containing the relevant shw information
    serialized_shws = []
    for shw, result in zip(shws, num_results):
        if shw.venue is None:
            continue
        num_seats_booked = shw.venue.num_total_seats - compute_reserved_seats(shw.id)
        if shw.movie and shw.venue:
            serialized_shw = {
                "id": shw.id,
                "day": shw.day.strftime('%Y-%m-%d'),
                "time": shw.time.strftime('%H:%M'),
                "movie": {
                    "id": shw.movie.id,
                    "title": shw.movie.title
                },
                "venue": {
                    "id": shw.venue.id,
                    "name": shw.venue.name,
                    "location": shw.venue.location,
                    "num_total_seats": shw.venue.num_total_seats,
                    "seats_available": num_seats_booked,
                    "seats_booked": compute_reserved_seats(shw.id),
                }
            }
            serialized_shws.append(serialized_shw)
        else:
           serialized_shw = {
                "id": shw.id,
                "day": shw.day.strftime('%Y-%m-%d'),
                "time": shw.time.strftime('%H:%M'),
            }
           serialized_shws.append(serialized_shw) 

    packed_data = [{"shw": serialized_shw, "result": result} for serialized_shw, result in zip(serialized_shws, num_results)]

    return jsonify(packed_data)


@blue.route("/delete_show/<int:show_id>", methods=["DELETE"])
@jwt_required()
@manager_only
def delete_show(show_id):
    show = model.shw.query.get(show_id)
    if not show:
        return jsonify({"success": False, "message": "Show not found."}), 404

    if request.method == 'DELETE':
        # Delete associated bookings
        bookings = model.booking.query.filter_by(shw_id=show_id).all()
        for booking in bookings:
            db.session.delete(booking)

        # Delete the show
        db.session.delete(show)
        db.session.commit()
        return jsonify({"success": True, "message": "Show and related bookings deleted successfully!"}), 200

    return jsonify({"success": False, "message": "Invalid request method."}), 405


@blue.route("/edit_show/<int:show_id>", methods=["POST"])
@jwt_required()
@manager_only
def edit_show(show_id):
    data = request.json

    show = model.shw.query.get(show_id)
    if not show:
        return jsonify({"success": False, "message": "Show not found."}), 404

    movie_id = data.get("movie_id")
    venue_id = data.get("venue_id")
    day = data.get("day")
    time = data.get("time")
    if not movie_id or not venue_id or not day or not time:
        return jsonify({"success": False, "message": "All fields are required."}), 400

    try:
        day = datetime.strptime(day, "%Y-%m-%d").date()
        time = datetime.strptime(time, "%H:%M:%S").time()
    except ValueError:
        return jsonify({"success": False, "message": "Invalid date or time format."}), 400

    show.day = day
    show.time = time
    show.movie_id = movie_id
    show.venue_id = venue_id

    db.session.commit()
    return jsonify({"success": True, "message": "Show edited successfully!"}), 200

@blue.route("/create_show", methods=["POST"])
@jwt_required()
@manager_only
def add_post():
    data = request.json
    movie_id = data.get("movieId")
    venue_id = data.get("venueId")
    day = datetime.strptime(data.get("day"), "%Y-%m-%d").date()
    time = datetime.strptime(data.get("time"), "%H:%M").time()

    new_shw = model.shw(day=day, time=time, movie_id=movie_id, venue_id=venue_id)
    db.session.add(new_shw)
    db.session.commit()

    return jsonify({"success": True, "message": "Show created successfully"})

@blue.route("/venue")
@jwt_required()
@manager_only
def list_venues():
    venues = model.Venue.query.all()
    serialized_venues = [venue_schema.dump(venue) for venue in venues]
    return jsonify(venues=serialized_venues)

@blue.route("/create_venue", methods=["POST"])
@jwt_required()
@manager_only
def create_venue():
    if request.method == 'POST':
        data = request.json
        name = data.get('name')
        location = data.get('location')
        num_total_seats = data.get("num_total_seats")

        if not name or not location or not num_total_seats:
            return jsonify({"success": False, "message": "All fields are required."}), 400

        new_venue = model.Venue(name=name, location=location, num_total_seats=num_total_seats)
        db.session.add(new_venue)
        db.session.commit()

        return jsonify({"success": True, "message": "New venue added successfully!"}), 200

    return jsonify({"success": False, "message": "Invalid request method."}), 405

@blue.route("/edit_venue/<int:venue_id>", methods=["POST"])
@jwt_required()
@manager_only
def edit_venue(venue_id):
    venue = model.Venue.query.get(venue_id)
    if request.method == 'POST':
        data = request.json
        name = data.get('name')
        location = data.get('location')
        num_total_seats = data.get("num_total_seats")

        if not name or not location or not num_total_seats:
            return jsonify({"success": False, "message": "All fields are required."}), 400

        venue.name = name
        venue.location = location
        venue.num_total_seats = num_total_seats
        db.session.commit()

        return jsonify({"success": True, "message": "Venue updated successfully!"}), 200

    return jsonify({"success": False, "message": "Invalid request method."}), 405


@blue.route("/delete_venue/<int:venue_id>", methods=["DELETE"])
@jwt_required()
@manager_only
def delete_venue(venue_id):
    venue = model.Venue.query.get(venue_id)
    if not venue:
        return jsonify({"success": False, "message": "Venue not found."}), 404

    if request.method == 'DELETE':
        db.session.delete(venue)
        db.session.commit()
        return jsonify({"success": True, "message": "Venue deleted successfully!"}), 200

    return jsonify({"success": False, "message": "Invalid request method."}), 405
    
@blue.route("/movie")
@jwt_required()
@manager_only
def list_movies():
    movies = model.Movie.query.all()
    serialized_movies = [movie_schema.dump(movie) for movie in movies]
    return jsonify(serialized_movies)


@blue.route('/create_movie', methods=['GET', 'POST'])
@jwt_required()
@manager_only
def create_movie():
    data = request.json
    title = data.get('title')
    director = data.get('director')
    duration = data.get('duration')
    cast = data.get('cast')
    rating = data.get('rating')
    price = data.get('price')
    img = data.get('img')

    if not title or not director or not duration or not cast or not rating or not price or not img:
        return jsonify({"error": "All fields are required."}), 400

    new_movie = model.Movie(title=title, director=director, duration=duration, cast=cast, rating=rating, price=price, img=img)
    db.session.add(new_movie)
    db.session.commit()

    return jsonify({"success": True, "message": "Movie created successfully"}), 200

@blue.route("/edit_movie/<int:movie_id>", methods=["GET", "POST"])
@jwt_required()
@manager_only
def edit_movie(movie_id):
    movie = model.Movie.query.get(movie_id)
    if not movie:
        return jsonify({"success": False, "message": "Movie not found."}), 404

    if request.method == 'POST':
        data = request.get_json()
        movie.title = data.get('title', movie.title)
        movie.director = data.get('director', movie.director)
        movie.duration = data.get('duration', movie.duration)
        movie.cast = data.get('cast', movie.cast)
        movie.rating = data.get('rating', movie.rating)
        movie.price = data.get('price', movie.price)
        movie.img = data.get('img', movie.img)

        db.session.commit()
        return jsonify({"success": True, "movie": movie_schema.dump(movie)}), 200

    return jsonify({"success": False, "message": "Invalid request method."}), 405

@blue.route("/delete_movie/<int:movie_id>", methods=["POST"])
@jwt_required()
@manager_only
def delete_movie(movie_id):
    movie = model.Movie.query.get(movie_id)
    if not movie:
        return jsonify({"error": "Movie not found."}), 404

    db.session.delete(movie)
    db.session.commit()
    return jsonify({"success": True, "message": "Movie deleted successfully"}), 200

@blue.route("/bookings")
@jwt_required()
@manager_only
def bookings():
    current_day = date.today()
    future = current_day + timedelta(days=7)
    past = current_day - timedelta(days=7)
    shws = model.shw.query.filter(model.shw.day <= future, model.shw.day >= past).order_by(model.shw.day.asc(), model.shw.time.asc()).all()
    bookings_data = []
    for sh in shws:
        if sh.venue is None:
            continue
        num_seats_booked = sh.venue.num_total_seats - compute_reserved_seats(sh.id)
        booking = {
            "show_id": sh.id,
            "title": sh.movie.title,
            "venue": sh.venue.name,
            "location": sh.venue.location,
            "total_seats": sh.venue.num_total_seats,
            "seats_available": num_seats_booked,
            "seats_booked": compute_reserved_seats(sh.id),
            "day": sh.day.strftime('%d-%m-%Y'),
            "time": sh.time.strftime('%H:%M')
        }
        bookings_data.append(booking)
    return jsonify(bookings_data)


@blue.route("/manage_booking/<int:id>")
@jwt_required()
@manager_only
def manage_booking(id):
    show = model.shw.query.get(id)
    booking = {
            "show_id": show.id,
            "title": show.movie.title,
            "venue": show.venue.name,
            "location": show.venue.location,
            "total_seats": show.venue.num_total_seats,
            "seats_available": show.venue.num_total_seats - compute_reserved_seats(show.id),
            "seats_booked": compute_reserved_seats(show.id),
            "day": show.day.strftime('%d-%m-%Y'),
            "time": show.time.strftime('%H:%M')
        }
    if not booking:
        return jsonify(message="No bookings found for this show.")
    return jsonify(booking=booking)


def manager_bookings_aux():
    current_day = date.today()
    future = current_day + timedelta(days=7)
    past = current_day - timedelta(days=7)
    shws = model.shw.query.filter(model.shw.day <= future, model.shw.day >= past).order_by(model.shw.day.asc(), model.shw.time.asc()).all()
    num_results = []
    for sh in shws:
        num_results.append(sh.venue.num_total_seats - compute_reserved_seats(sh.id))
    return shws, num_results


def compute_reserved_seats(id):
    shw = model.shw.query.filter(model.shw.id == id).one()
    sum_result = db.session.query(
        db.func.sum(model.booking.num_seats).label('reserved')
    ).filter(
        model.booking.shw == shw
    ).one()
    num_reserved_seats = sum_result.reserved
    if (sum_result.reserved != None):
        num_free_seats = shw.venue.num_total_seats - num_reserved_seats
    else:
        num_free_seats = shw.venue.num_total_seats         
    return  num_free_seats