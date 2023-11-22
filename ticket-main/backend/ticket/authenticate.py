from flask import Blueprint, render_template, request, redirect, url_for, flash
import flask_login
from . import model
from flask import jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .db import db as db_instance
from . import bcrypt

db = db_instance.database

blue = Blueprint("authenticate", __name__)
@blue.route("/signup", methods=["POST"])
def signup_post():
    data = request.get_json()  # Parse the JSON data from the request body
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")
    role = data.get("role")
    
    user = model.User.query.filter_by(email=email).first()
    if user:
        return {"error": True, "message": "Email you provided is already registered"}, 400

    if role == 'manager':
        role = model.UserRole.manager
    else:
        role = model.UserRole.customer

    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    new_user = model.User(email=email, name=username, password=password_hash, role=role)
    db.session.add(new_user)
    db.session.commit()
    return {"error": False, "message": "You have successfully signed up"}


@blue.route("/login", methods=["POST"])
def login_post():
    data = request.get_json()  # Parse the JSON data from the request body
    email = data.get("email")
    password = data.get("password")
    user = model.User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        accessToken = create_access_token(identity=str(user.id))
        response = jsonify({"error": False, "accessToken": accessToken})
        return response
    else:
        if user == None:
            return {"error": True, "message": "Invalid credentials"}, 401
        if user.email == email and bcrypt.check_password_hash(user.password, password) == 0:
            return {"error": True, "message": "Invalid Password"}, 401

@blue.route("/users", methods=["GET"])
def get_all_users():
    user = model.User.query.all()
    response = jsonify(user)
    return response

@blue.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()  
    return {'message': 'You have been logged out', 'success': True}
