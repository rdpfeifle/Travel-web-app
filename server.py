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


##--------------------- 404 ERROR HANDLER - PAGE NOT FOUND ---------------------##

@app.errorhandler(404)
def page_not_found(e):

    logged_in = session.get("user_id") # it was giving me an error without this

    return render_template("404.html", logged_in=logged_in)


##--------------------- USER'S LOGIN PAGE ---------------------##

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
        return redirect("/user-account")


##--------------------- USER'S SIGN UP PAGE ---------------------##

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
        
        return redirect("/user-account")


##--------------------- USER'S LOGOUT ---------------------##

@app.route("/logout")
def logout():
    """Log out from account."""

    if "user_id" in session:
        flash("You have been logged out!", "success")
    session.pop("user_id", None)

    return redirect("/")


##--------------------- USER'S PERSONAL ACCOUNT ---------------------##

@app.route("/user-account")
def user_account():
    """Show user's personal account."""

    # logged_in = session.get("user_id") # checking if the user is logged in
    user_id = session.get("user_id") # checking if the user is already in session
    user = crud.get_user_by_id(user_id)
    trips = user.trips

    return render_template("user-account.html", user_id=user_id, trips=trips, fname=user.fname, YOUR_API_KEY=api_key)


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
    trip_title = request.form.get("trip_title")
    destination = request.form.get("destination")
    # start_date = request.form.get("start_date")
    # end_date = request.form.get("end_date")
    dates = request.form.get("dates").split()
    start_date = datetime.strptime(dates[0], "%Y-%m-%d")
    end_date = datetime.strptime(dates[2], "%Y-%m-%d")

    logged_in = session.get("user_id")

    if logged_in:
        trip = crud.create_trip(logged_in, trip_title, destination, start_date, end_date)
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

    # logged_in = session.get("user_id")
    trip = crud.get_trip_by_id(trip_id)
    reservations = trip.reservations
    
    # add tasks here
    task_list = trip.tasks

    if "user_id" not in session:
        flash("Please, log into your existent account or create one.", "error")
        return redirect("/")

    return render_template("details.html", trip=trip, reservations=reservations, task_list=task_list)


################### CHECKLIST ROUTES ###################

@app.route("/add-task", methods=["POST"])
def add_task():
    """Add new task."""

    trip_id = request.form.get("trip_id")
    task_title = request.form.get("task_title")

    new_task = crud.create_task(task_title=task_title)

    db.session.add(new_task)
    db.session.commit()

    return redirect(f"/details/{trip_id}")


@app.route("/edit-task/<int:checklist_id>")
def edit_task(checklist_id):
    """Edit a task."""

    # select the task by its ID
    task = crud.get_task_by_id(checklist_id)

    # switch task from True => False and False => True (completed or not)
    task.completed = not task.completed

    db.session.commit()

    return redirect("/details")


@app.route("/delete-task/<int:checklist_id>")
def delete_task(checklist_id):
    """Delete a task."""

    # select the task by its ID
    task = crud.get_task_by_id(checklist_id)

    db.session.delete(task)
    db.session.commit()

    return redirect("/details")


################### ADD A RESERVATION ###################

@app.route("/add-reservation", methods=["POST"])
def save_reservation():

    trip_id = request.form.get("trip_id")
    confirmation_info = request.form.get("confirmation_info")
    reservation_type = request.form.get("reservation_type")
    destination = request.form.get("destination")
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")
    notes = request.form.get("notes")

    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    trip = crud.get_trip_by_id(trip_id)

    if start_date < trip.start_date or end_date > trip.end_date:
        flash("Please enter reservation dates within your trip dates.", "error")
        return redirect(f"/details/{trip_id}")

    reservation = crud.create_reservation(trip_id,reservation_type, confirmation_info, destination, start_date, end_date, notes)

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
        flash(f"Trip to {trip_to_delete.destination} was deleted successfully.", "success")
        return render_template("/user-account.html")

    except:
        return redirect("/user-account")


################### EDIT TRIPS ###################

@app.route("/user-account/edit-trip/<int:trip_id>", methods=["GET"])
def display_edit_trip_page(trip_id):
    """Display edit trips' page """

    return render_template("edit-trip.html", trip_id=trip_id)


@app.route("/user-account/edit-trip/<int:trip_id>", methods=["POST"])
def edit_trip(trip_id):
    """Edit trip info."""

    trip_to_edit = crud.get_trip_by_id(trip_id)

    trip_title = request.form.get("trip_title")
    description = request.form.get("description")

    if "user_id" in session:

        # if the trip title from the form is NOT empty
        # assign value given in the form to the trip_title in the database
        if trip_title != "":
            trip_to_edit.trip_title = trip_title
        
        if description != "":
            trip_to_edit.description = description

        # then commit to the db
        db.session.commit()

        return redirect("/user-account")

    return redirect("/")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)