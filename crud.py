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


def create_trip_date(start_date, end_date):
    """Create trip days by subtracting end date with start date."""

    trip_dates = []

    duration = end_date - start_date

    for day in range(duration.days + 1):
        date = start_date + timedelta(days=day)
        trip_dates.append(date)

    return trip_dates


########### Activity Functions ###########

def create_new_activity():
    """Create a new activity."""

    pass


########### Reservation Functions ###########


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