"""Server for travel web app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
import os
import argon2
from argon2 import PasswordHasher
ph = PasswordHasher()
import crud
import requests
from jinja2 import StrictUndefined
from datetime import timedelta, datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)

app.secret_key = "hellohello"

api_key = os.environ['YOUR_API_KEY']
UNSPLASH_SECRET_KEY = os.environ['UNSPLASH_KEY']

app.jinja_env.undefined = StrictUndefined
app.app_context().push()

##--------------------- HOMEPAGE ---------------------##

@app.route("/")
def homepage():
    """View homepage."""

    logged_in = session.get("user_id")

    images = crud.get_images_of_places()

    return render_template("homepage.html", logged_in=logged_in, images=images)


##------------------- USER'S LOGIN PAGE -------------------##

@app.route("/login")
def show_login():
    """Shows log in page."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Process user login."""

    email = request.form.get("email")
    password = request.form.get("password")
    
    user = crud.get_user_by_email(email)

    try:

        # check by hashed password
        if ph.verify(user.password, password):

            session["user_id"] = user.user_id
            session["email"] = email

            flash("You were logged in.", "success")

            return redirect("/my-trips")

    # if not user, flash an error message and redirect to login page
    except:

        flash("The email or password you entered was incorrect. Please try again.", "error")

        return redirect("/login")


##--------------------- SIGN UP PAGE ---------------------##

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

    existing_user = crud.get_user_by_email(email)

    # adding hash password here
    hashed_password = ph.hash(password)
    
    if existing_user:
        flash("Account already exists. Please log in.", "error")
        return redirect("/login")
      
    else:
        user = crud.create_user(
            fname=fname,
            lname=lname,
            email=email, 
            password=hashed_password
            )
        print("#########")
        print(user)
        print(user.password)
        print("########")

        db.session.add(user)
        db.session.commit()

        # adding user_id to the log in session
        session["user_id"] = user.user_id

        flash(f"Account created successfully, {fname}.", "success")
        
        return redirect("/my-trips")


##--------------------- USER'S LOGOUT ---------------------##

@app.route("/logout")
def logout():
    """Log out from account."""

    if "user_id" in session:
        flash("You have been logged out!", "success")
    session.pop("user_id", None)

    return redirect("/")


##---------------- USER'S PERSONAL ACCOUNT ----------------##

@app.route("/account")
def user_account():
    """Show user's personal account."""

    user_id = session.get("user_id")
    user = crud.get_user_by_id(user_id)

    if "user_id" in session:
        return render_template("account.html", fname=user.fname, email=user.email)

    else:
        return redirect("/")


@app.route("/edit-account", methods=["POST"])
def edit_user_account():
    """Edit user info."""

    first_name = request.form.get("fname")
    email = request.form.get("email")

    # grab user from session
    user_id = session.get("user_id")

    # users
    existent_user = crud.get_user_by_email(email)

    user = crud.get_user_by_id(user_id)

    if "user_id" in session:

        if first_name != "":
            user.fname = first_name

            # then commit to the db
            db.session.commit()

        if not existent_user and email != "":
            user.email = email
            db.session.commit()
                
        else:
            flash("That email already exists.", "error")

        return redirect("/my-trips")
    
    return redirect("/")


##--------------------- PLAN A TRIP ---------------------##

@app.route("/plan-trip")
def plan_trip():
    """Display 'plan a new trip' page."""

    logged_in = session.get("user_id")

    return render_template("plan-trip.html", logged_in=logged_in)


@app.route("/plan-trip", methods=["POST"])
def add_trip():
    """Create and add a trip to the user's account."""

    trip_title = request.form.get("trip_title")
    destination = request.form.get("destination")
    dates = request.form.get("dates").split()
    start_date = datetime.strptime(dates[0], "%Y-%m-%d")
    end_date = datetime.strptime(dates[2], "%Y-%m-%d")

    # unsplash API call here
    url = "https://api.unsplash.com/search/photos"

    # query is our chosen destination
    # client_id is my API key
    # orientation could be portrait or landscape, but I like landscape :)
    payload = {
        "query": destination,
        "client_id": UNSPLASH_SECRET_KEY,
        "orientation": "landscape",
    }

    # save response from my API request
    response = requests.get(url, params=payload)

    # turns JSON into a Python dict
    data = response.json()
    # print(data) # testing

    # get data from data dict and get key called "results"
    get_key_results = data.get("results")
    # print(get_key_results) # testing

    # I should try to get the alt description for my HTML template: alt_description => get_key_results = data.get("alt_description")

    # results is a list that contains dictionaries within
    # urls is a key with a value of dictionary containing key-value pairs with imgs sizes

    # get img url
    img_url = get_key_results[0].get("urls")
    # print(img_url)

    # get the img url with full size
    destination_img = img_url.get("regular")
    # print(destination_img) # testing

    logged_in = session.get("user_id")

    if logged_in:
        trip = crud.create_trip(logged_in, trip_title, destination, start_date, end_date, img=destination_img)
        db.session.add(trip)
        db.session.commit()

    else:
        flash("Please, log into to start planning your trip.", "warning")
        return redirect("/")

    # return redirect(f"/details/{trip.trip_id}")
    return redirect("/my-trips")


##----------------- DISPLAY TRIP DETAILS -----------------##

@app.route("/details/<int:trip_id>", methods=["GET"])
def display_trip_details(trip_id):
    """Display trip details."""

    # logged_in = session.get("user_id")
    trip = crud.get_trip_by_id(trip_id)
    reservations = trip.reservations
    activities = trip.activities
    
    # add tasks here
    task_list = trip.tasks

    if "user_id" not in session:
        flash("Please, log into your existent account or create one.", "error")
        return redirect("/")

    return render_template("details.html", trip=trip, task_list=task_list, activities=activities, reservations=reservations, YOUR_API_KEY=api_key)


##--------------------- USER'S TRIPS ---------------------##

@app.route("/my-trips")
def user_trips():
    """Show user's trips."""

    try:
        user_id = session.get("user_id") # checking if the user is already in session
        user = crud.get_user_by_id(user_id)
        trips = user.trips

        return render_template("my-trips.html", user_id=user_id, trips=trips, fname=user.fname, YOUR_API_KEY=api_key)

    except:
        return redirect("/login")


@app.route("/delete-trip", methods=["POST"])
def delete():
    """Delete a trip."""

    trip_to_delete = request.json.get("tripToDelete")

    trip = crud.get_trip_by_id(trip_to_delete)

    try:
        db.session.delete(trip)
        db.session.commit()
        return "Success"

    except:
        return "Could not delete trip."


@app.route("/my-trips/edit-trip/<int:trip_id>", methods=["GET"])
def display_edit_trip_page(trip_id):
    """Display edit trips' page """

    return render_template("edit-trip.html", trip_id=trip_id)


@app.route("/my-trips/edit-trip/<int:trip_id>", methods=["POST"])
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

        return redirect("/my-trips")

    return redirect("/")


##------------------- CHECKLIST ROUTES -------------------##

@app.route("/add-task", methods=["POST"])
def add_task():
    """Add new task."""

    trip_id = request.form.get("trip_id")
    task_title = request.form.get("task_title")
    completed = request.form.get("completed")

    new_task = crud.create_task(
    trip_id,
    task_title,
    completed=completed,
    )

    print(new_task)

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

    return redirect(f"/details/{task.trip_id}")


@app.route("/delete-task/<int:checklist_id>")
def delete_task(checklist_id):
    """Delete a task."""

    # select the task by its ID
    task = crud.get_task_by_id(checklist_id)

    db.session.delete(task)
    db.session.commit()

    return redirect(f"/details/{task.trip_id}")

##--------------------- INVITE A FRIEND ---------------------##

@app.route("/invite-friend", methods=["POST"])
def invite_friend_by_email():
    """Send invitation to friend by email."""

    # get info from form
    friend_trip_id = request.form.get("friend-trip-id")
    friends_email = request.form.get("friends-email")

    user_id = session.get("user_id")
    # get user who invited their friend
    user = crud.get_user_by_id(user_id)

    # access trip from db
    trip = crud.get_trip_by_id(friend_trip_id)

    trip_start_date = str(trip.start_date)
    start_date = datetime.strptime(trip_start_date, "%Y-%m-%d")
    start_date = start_date.strftime("%b %d, %Y")

    # check if friend is already a user
    # is_friend_a_user = crud.get_user_by_email(friends_email)

    # if not is_friend_a_user:
    #     flash("Your friend doesn't have an account.", "error")

    message = Mail(
    from_email='raquelpfeifle@gmail.com',
    to_emails=friends_email,
    subject=f'Your friend invited you to travel with them.',
    html_content=f'Hey there! Your friend is inviting you to travel together. They are traveling to {trip.destination} on {start_date}. Please, sign up or login into your existent account to start planning.')

    # subject=f'{user.fname} invited you to travel with them.',
    # html_content=f'Hey there! Your friend {user.fname} is inviting you to travel together. {user.fname} traveling to {trip.destination} on {trip.start_date.date()}. Please, create an account to see more.' => this was giving me an attribute error

    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)

    return redirect(f"/details/{friend_trip_id}")


##------------------- RESERVATION ROUTES -------------------##

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

    print(reservation)

    db.session.add(reservation)
    db.session.commit()

    flash("Your reservation was created successfully.", "success")

    return redirect(f"/details/{trip_id}")


@app.route("/delete-reservation", methods=["POST"])
def delete_reservation():
    """Delete a reservation."""

    reservation_to_delete = request.json.get("reservation_to_delete")

    reservation = crud.get_reservation_by_id(reservation_to_delete)

    try:
        db.session.delete(reservation)
        db.session.commit()
        return "Success"

    except:
        return "Could not delete reservation."


##------------------- ACTIVITIES ROUTES -------------------##

@app.route("/add-activity", methods=["POST"])
def add_activity():
    """Add a activity."""

    trip_id = request.form.get("trip_id")
    activity_type = request.form.get("activity_type")
    place_name = request.form.get("place_name")
    datetime = request.form.get("dateTime")
    address = request.form.get("address")
    phone_number = request.form.get("phone_number")
    comments = request.form.get("comments")

    # unsplash API call here
    url = "https://api.unsplash.com/search/photos"

    payload = {
        "query": place_name,
        "client_id": UNSPLASH_SECRET_KEY,
        "orientation": "landscape",
    }

    # save response from my API request
    response = requests.get(url, params=payload)

    # turns JSON into a Python dict
    data = response.json()

    # get data from data dict and get key called "results"
    get_key_results = data.get("results")

    img_url = get_key_results[0].get("urls")
    print(img_url)

    # get the img url with full size
    place_image = img_url.get("regular")
    print(place_image) # testing

    activity = crud.create_activity(
        trip_id=trip_id,
        activity_type=activity_type,
        place_name=place_name,
        datetime=datetime,
        address=address,
        phone_number=phone_number,
        comments=comments,
        place_img=place_image
    )

    db.session.add(activity)
    db.session.commit()

    return redirect(f"/details/{trip_id}")


@app.route("/delete-activity", methods=["POST"])
def delete_activity():
    """Delete an activity."""

    activity_to_delete = request.json.get("activity_to_delete")

    activity = crud.get_activity_by_id(activity_to_delete)

    try:
        db.session.delete(activity)
        db.session.commit()
        return "Success"

    except:
        return "Could not delete activity."


##---------- 404 ERROR HANDLER - PAGE NOT FOUND ----------##

@app.errorhandler(404)
def page_not_found(e):

    logged_in = session.get("user_id") # it was giving me an error without this

    return render_template("404.html", logged_in=logged_in)



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0")

    #debug=True