"""Server for travel web app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
import os
from passlib.hash import argon2
import crud
import requests
from jinja2 import StrictUndefined
from datetime import timedelta, datetime

app = Flask(__name__)

app.secret_key = "hellohello"

api_key = os.environ['YOUR_API_KEY']
UNSPLASH_SECRET_KEY = os.environ['UNSPLASH_KEY']
YELP_SECRET_KEY = os.environ['YELP_KEY']

app.jinja_env.undefined = StrictUndefined
app.app_context().push()


@app.route("/")
def homepage():
    """View homepage."""

    logged_in = session.get("user_id")

    return render_template("homepage.html", logged_in=logged_in)


################### 404 ERROR HANDLER - PAGE NOT FOUND ###################

@app.errorhandler(404)
def page_not_found(e):

    logged_in = session.get("user_id") # it was giving me an error without this

    return render_template("404.html", logged_in=logged_in)


################### USER'S LOGIN PAGE ###################

@app.route("/login")
def show_login():
    """Shows log in page."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Process user login."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email_and_pass(email, password)

    # if not user, flash an error message and redirect to login page
    if not user or user.password != password:
        flash("The email or password you entered was incorrect. Please try again.", "error")
        return redirect("/login")

    # otherwise, redirect to user's account
    else:
        flash("You were logged in.", "success")
        session["user_id"] = user.user_id
        return redirect("/user_account")


################### USER'S SIGN UP PAGE ###################

@app.route("/signup")
def show_signup():
    """Shows sign up page."""

    return render_template("signup.html")


@app.route("/signup", methods=["POST"])
def register_user():
    """Create a new user."""
    
    fname = request.form.get("fname")
    lname = request.form.get("lname")
    email = request.form.get("email")
    password = request.form.get("password")

    existing_user = crud.get_user_by_email_and_pass(email, password)

    # adding hash password here
    hashed_password = argon2.hash(password)
    del password
    
    if existing_user:
        flash("Account already exists. Please log in.", "error")
        return redirect("/signup")
      
    else:
        user = crud.create_user(
            fname=fname,
            lname=lname,
            email=email, 
            password=hashed_password
            )
        
        db.session.add(user)
        db.session.commit()

        # adding user_id to the log in session
        session["user_id"] = user.user_id

        flash(f"Account created successfully, {fname}.", "success")
        
        return redirect("/user_account")


################### USER'S LOGOUT ###################

@app.route("/logout")
def logout():
    """Log out from account."""

    if "user_id" in session:
        flash("You have been logged out!", "success")
    session.pop("user_id", None)

    return redirect("/")


################### USER'S PERSONAL ACCOUNT ###################

@app.route("/user_account")
def user_account():
    """Show user's personal account."""

    logged_in = session.get("user_id") # checking if the user is logged in
    user_id = session.get("user_id") # checking if the user is already in session
    user = crud.get_user_by_id(user_id)
    trips = user.trips

    return render_template("user_account.html", user_id=user_id, trips=trips, fname=user.fname, logged_in=logged_in, YOUR_API_KEY=api_key)


################### PLAN A NEW TRIP ###################

@app.route("/plan-trip")
def plan_trip():
    """Display 'plan a new trip' page."""

    logged_in = session.get("user_id")

    return render_template("plan-trip.html", logged_in=logged_in)


@app.route("/plan-trip", methods=["POST"])
def add_trip():
    """Create and add a trip to the user's account."""

    # traveler = request.form.get("traveler")
    destination = request.form.get("destination")
    # start_date = request.form.get("start_date")
    # end_date = request.form.get("end_date")
    dates = request.form.get("dates").split()
    start_date = datetime.strptime(dates[0], "%Y-%m-%d")
    end_date = datetime.strptime(dates[2], "%Y-%m-%d")

    logged_in = session.get("user_id")

    if logged_in:
        trip = crud.create_trip(logged_in, destination, start_date, end_date)
        db.session.add(trip)
        db.session.commit()

    else:
        flash("Please, log into to start planning your trip.", "warning")
        return redirect("/")

    return redirect(f"/details/{trip.trip_id}")


################### ADD ACTIVITIES TO THE TRIP'S PLAN ###################

@app.route("/details/<int:trip_id>", methods=["GET"])
def display_trip_details(trip_id):
    """Display trip details."""

    logged_in = session.get("user_id")
    trip = crud.get_trip_by_id(trip_id)
    reservations = trip.reservations

    if "user_id" not in session:
        flash("Please, log into your existent account or create one.", "error")
        return redirect("/")

    return render_template("details.html", logged_in=logged_in, trip=trip, reservations=reservations)


################### ADD A RESERVATION ###################

@app.route("/add-reservation", methods=["POST"])
def save_reservation():

    trip_id = request.form.get("trip_id")
    confirmation_num = request.form.get("confirmation_num")
    reservation_type = request.form.get("reservation_type")
    destination = request.form.get("destination")
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")

    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    # datetime.strptime(dates[0], "%Y-%m-%d")

    print(type(start_date))
    print(type(start_date))
    trip = crud.get_trip_by_id(trip_id)

    if start_date < trip.start_date or end_date > trip.end_date:
        flash("Invalid reservation dates. Please try again.", "error")
        return redirect(f"/details/{trip_id}")

    reservation = crud.create_reservation(trip_id,reservation_type, confirmation_num, destination, start_date, end_date)

    db.session.add(reservation)
    db.session.commit()

    flash("Your reservation was created successfully.", "success")

    return redirect(f"/details/{trip_id}")


################### DELETE TRIPS ###################

@app.route("/delete/<int:trip_id>")
def delete(trip_id):
    """Delete a trip."""

    trip_to_delete = crud.get_trip_by_id(trip_id)

    try:
        db.session.delete(trip_to_delete)
        db.session.commit()
        flash("Trip deleted successfully.", "warning")
        return render_template("/user_account.html")

    except:
        return redirect("/user_account")


################### EDIT TRIPS ###################

@app.route("/user_account/<int:trip_id>/edit-trip", methods=["GET", "POST"])
def edit_trip(trip_id):
    """Edit trip info."""

    trip_to_edit = crud.get_trip_by_id(trip_id)

    if "user" in session:
        db.session.update(trip_to_edit)
        db.session.commit()

        return render_template(f"/user_account/{trip_to_edit.trip_id}/edit-trip.html")

    return redirect("/user_account")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)