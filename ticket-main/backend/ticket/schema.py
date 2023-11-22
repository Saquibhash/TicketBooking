from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Integer()
    email = fields.String()
    name = fields.String()
    role = fields.String()

class MovieSchema(Schema):
    id = fields.Integer()
    title = fields.String()
    director = fields.String()
    duration = fields.Integer()
    cast = fields.String()
    rating = fields.Integer()
    price = fields.Integer()
    img = fields.String()

class ShowtimeSchema(Schema):
    id = fields.Integer()
    day = fields.Date()
    time = fields.Time()
    movie_id = fields.Integer()
    venue_id = fields.Integer()
    
class VenueSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    location = fields.String()
    num_total_seats = fields.Integer()

class Booking(Schema):
    id = fields.Integer()
    user_id = fields.Integer()
    shw_id = fields.Integer()
    num_seats = fields.Integer()

venue_schema = VenueSchema()
user_schema = UserSchema()
movie_schema = MovieSchema()
showtime_schema = ShowtimeSchema()
booking_schema = Booking()