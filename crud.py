"""CRUD operations."""

from model import db, User, Trip, Activity, Reservation, Image, connect_to_db
from passlib.hash import argon2
from datetime import timedelta


########### User Functions ###########

def create_user(fname, lname, email, password):
    """Create and return a new user."""

    user = User(fname=fname,
                lname=lname,
                email=email, 
                password=password)

    return user


def get_users():
    """Return all users."""

    return User.query.all()


def get_user_by_name(fname):
    """Return a user by their first name."""

    return User.query.filter_by(fname).first()

    
def get_user_by_id(user_id):
    """Return a user by primary key."""

    return User.query.get(user_id)


def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()


def get_user_by_email_and_pass(email, password):
    """Return a user by email and password."""

    return User.query.filter(User.email == email, User.password == password).first()


def hashed_password(password):
    """Converts the users' passwords to hash."""

    return argon2.hash(password)


########### Trip Functions ###########

def create_trip(traveler, destination, start_date, end_date):
    """Create and return new trip."""

    trip = Trip(
        traveler=traveler,
        destination=destination,
        trip_title=destination,
        start_date=start_date,
        end_date=end_date,
    )

    return trip


def get_trip_by_id(trip_id):
    """Return trip information by getting the trip id."""

    return Trip.query.get(trip_id)


# def get_trip_by_destination(destination):
#     """Return trip by destination."""

#     return User.query.filter(Trip.destination == destination).first()


########### Edit trips ###########

def delete_trip(trip_id):
    """Delete trip from database."""

    return Trip.query.delete(trip_id)





########### Edit trips ###########

def update_trip(trip_id, new_destination, new_start_date, new_end_date):
    """Update trip info given trip_id and the new info."""

    trip = Trip.query.get(trip_id)
    trip.destination = new_destination
    trip.start_date = new_start_date
    trip.end_date = new_end_date

########### Activity Functions ###########

def create_new_activity():
    """Create a new activity."""

    pass


########### Reservation Functions ###########
def create_reservation(trip_id, reservation_type, confirmation_num, destination, start_date, end_date):
    """Create and return new reservation."""

    reservation = Reservation(
        trip_id=trip_id,
        reservation_type=reservation_type,
        confirmation_num=confirmation_num,
        location=destination,
        start_date=start_date,
        end_date=end_date,
    )

    return reservation

########### Image Functions ###########

def image_displays():
    """Display images from places to visit on homepage."""

    pass

############# Places for the homepage

# def get_images_of_places():
#     """Return all images."""

#     return Image.query.all()

# def get_image_by_id(img_id):
#     """Return an image by primary key."""

#     return Image.query.get(img_id)

if __name__ == '__main__':
    from server import app
    connect_to_db(app)