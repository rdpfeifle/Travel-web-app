"""CRUD operations."""

from model import db, User, Trip, Activity, Reservation, connect_to_db


########### User Functions ###########

def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user


def get_users():
    """Return all users."""

    return User.query.all()


def get_user_by_id(user_id):
    """Return a user by primary key."""

    return User.query.get(user_id)


def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()


########### Trip Functions ###########

def create_trip(traveler, destination, country_name, trip_title, start_date, end_date, img):
    """Create and return new trip."""

    trip = Trip(
        traveler=traveler,
        destination=destination,
        country_name=country_name,
        trip_title=trip_title,
        start_date=start_date,
        end_date=end_date,
        img=img
    )

    return trip


def get_trip_by_id(trip_id):
    """Return trip information by getting the trip id."""

    return Trip.query.get(trip_id)


def create_trip_date():
    """Create trip """

    return None

########### Activity Functions ###########
def create_new_activity():
    """Create a new activity."""
    return None

########### Reservation Functions ###########

########### Image Functions ###########

if __name__ == '__main__':
    from server import app
    connect_to_db(app)