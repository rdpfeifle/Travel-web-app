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

    logged_in = session.get("user_id")

    return render_template("homepage.html", logged_in=logged_in)


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

    # if not user, flash a message and redirect to login page
    if not user or user.password != password:
        flash("The email or password you entered was incorrect. Please try again.")
        return redirect("/login")

    # otherwise, redirect to user's account
    else:
        flash("Logged in.")
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
    
    if existing_user:
        flash("Account already exists. Please log in.")
        return redirect("/signup")
    else:
        user = crud.create_user(
            fname=fname,
            lname=lname,
            email=email, 
            password=password
            )
        
        db.session.add(user)
        db.session.commit()

        # adding user_id to the log in session
        session["user_id"] = user.user_id

        flash(f"Account created successfully, {fname}.")
        
        return redirect("/user_account")


################### USER'S LOGOUT ###################

@app.route("/logout")
def logout():
    """Log out from account."""

    if "user_id" in session:
        flash("You have been logged out!")
    session.pop("user_id", None)

    return redirect("/")


################### USER'S PERSONAL ACCOUNT ###################

@app.route("/user_account")
def user_account():
    """Show user's personal account."""

    logged_in = session.get("user_id") # checking if the user is logged in
    user_id = session.get("user_id") # checking if the user is already in session
    user = crud.get_user_by_id(user_id)

    return render_template("user_account.html", user_id=user_id, fname=user.fname, logged_in=logged_in)



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)