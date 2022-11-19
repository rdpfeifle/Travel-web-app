"""CRUD operations."""

from model import db, User, Trip, Activity, Reservation, Checklist, Image, connect_to_db
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

def create_trip(traveler, trip_title, destination, start_date, end_date, img):
    """Create and return new trip."""

    trip = Trip(
        traveler=traveler,
        trip_title=trip_title,
        destination=destination,
        start_date=start_date,
        end_date=end_date,
        img=img,
    )

    return trip


def get_trip_by_id(trip_id):
    """Return trip information by getting the trip id."""

    return Trip.query.get(trip_id)


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
def create_reservation(trip_id, reservation_type, confirmation_info, destination, start_date, end_date, notes):
    """Create and return new reservation."""

    reservation = Reservation(
        trip_id=trip_id,
        reservation_type=reservation_type,
        confirmation_info=confirmation_info,
        location=destination,
        start_date=start_date,
        end_date=end_date,
        notes=notes,
    )

    return reservation


def get_reservation_by_id(reservation_id):
    """Return trip information by getting the trip id."""

    return Reservation.query.get(reservation_id)


########### Checklist Functions ###########

def get_tasks_by_trip_id(trip_id):
    """Return all tasks by trip id."""

    return Checklist.query.filter(Checklist.trip_id==trip_id).all()


def get_task_by_id(checklist_id):
    """Return a task by id."""

    return Checklist.query.get(checklist_id)


def create_task(trip_id, task_title, completed):
    """Create a task."""

    task = Checklist(
        trip_id=trip_id,
        task_title=task_title,
        completed=completed,
    )

    return task

########### Activities Functions ###########
def create_activity(trip_id, activity_type, place_name, datetime, address, phone_number, comments):
    """Create and return an activity."""

    activity = Activity(trip_id=trip_id,
                        activity_type=activity_type,
                        place_name=place_name,
                        datetime=datetime,
                        address=address,
                        phone_number=phone_number,
                        comments=comments,
                        )
    return activity


def get_activity_by_id(activity_id):
    """Return activity information by getting the activity id."""

    return Activity.query.get(activity_id)

########### Image Functions ###########

def create_image(place_name, city_name, description, url):
    """Create images from places to visit on homepage."""

    image = Image(
        place_name=place_name,
        city_name=city_name,
        description=description,
        url=url,
    )

    return image


def get_images_of_places():
    """Return all images."""

    return Image.query.all()


def get_image_by_id(img_id):
    """Return an image by primary key."""

    return Image.query.get(img_id)


if __name__ == '__main__':
    from server import app
    connect_to_db(app)