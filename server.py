"""Server for travel web app."""

from flask import Flask, render_template, request, flash, session, redirect, url_for
from model import connect_to_db, db
import crud
import os
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
# api_key = os.environ['GM_API_KEY']

app.jinja_env.undefined = StrictUndefined
app.app_context().push()

@app.route("/")
def homepage():
    """View homepage."""
    return render_template("homepage.html")


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

    # if not user, flash a message and redirect to login page
    if not user or user.password != password:
        flash("The email or password you entered was incorrect. Please try again.")
        return redirect("/login")

    # otherwise, redirect to user's account
    else:
        flash("Logged in.")
        session["user_id"] = user.user_id
        return redirect("/user_account")


@app.route("/signup")
def show_signup():
    """Show sign up page."""

    return render_template("signup.html")


@app.route("/signup", methods=["POST"])
def register_user():
    """Create a new user."""
    
    fname = request.form.get("fname")
    lname = request.form.get("lname")
    email = request.form.get("email")
    password = request.form.get("password")

    existing_user = crud.get_user_by_email_and_pass(email, password)
    
    if existing_user:
        flash("Account already exists. Please log in.")
        return redirect("/signup")
    else:
        user = crud.create_user(
            fname=fname,
            lname=lname,
            email=email, 
            password=password)
        
        db.session.add(user)
        db.session.commit()

        # adding user id to the session
        session["user_id"] = user.user_id
        flash(f"Account created successfully, {fname}.")
        return redirect("/user_account")


@app.route("/logout")
def logout():
    if "user_id" in session:
        flash("You have been logged out!")
    session.pop("user_id", None)
    return redirect("/login")

@app.route("/user_account")
def user_account():
    
    user_id = session.get("user_id")
    user = crud.get_user_by_id(user_id)

    return render_template("user_account.html", user_id=user_id, fname=user.fname)

        
############# Places for the homepage

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)