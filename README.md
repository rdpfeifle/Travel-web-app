# Tripaholics

## Table of Contents

- [Technologies](#technologies-used)
- [Features](#features)
- [Future Improvements](#future-improvements)
- [Set Up](#set-up)
- [About Me](#about-me)

## Technologies Used

- Front-end: Javascript, HTML5, CSS3, Bootstrap, AJAX, JSON
- Templating Engine: Jinja2
- Back-end: Python, Flask, PostgreSQL, SQLAlchemy
- APIs: Google Maps API, Twilio's SendGrid API, Unsplash Images API, Swiper API

## Features

- ✨[Watch demo video](https://youtu.be/c5srainYwKA)
- 💻 [Check deployed website](http://54.149.223.126/)

### Homepage

- Homepage displays additional information about the project, including a navbar that automatically scrolls down when a link is clicked
- Users can click on the button to start planning, but they can create a trip only if they are logged in
- Users can see recommended places to travel to in a beautiful carousel
- Users can read provided answers to a list of frequently asked questions about the project

  ![Tripaholics - Homepage](/static/screenshots/homepage.gif)

### Sign up/Login

- Users can create an account and/or login
- Passwords are saved to the database already hashed for extra layer of security using Argon2

  ![Tripaholics - Sign Up](/static/screenshots/signup-page.png)

### My Trips Page

- Trips created are displayed as cards. If users click on the card, they are redirected to the Trip Details Page, where they can add a task to their to-do list, as well as reservations, activities, and send an invitation to their friends so they can join the trip.
- Users can choose to edit or delete a particular trip if they want to. I used AJAX for the delete button to delete the trip without reloading the page.
- If users click to edit a trip, they are redirected to the "Edit Trip" page where they can modify or add the reason of the trip, as well as a description.

  ![Tripaholics - My Trips](/static/screenshots/my-trips.gif)

### Edit Trip Page

- Users can modify or add the reason of the trip, as well as a description, and save the changes to the db.

  ![Tripaholics - Edit Trip](/static/screenshots/edit-trip.png)

### Account Page

- Users can edit their account information by clicking "Account" on the navbar. They can change their name or email, and save the changes to the database.

  ![Tripaholics - My Account](/static/screenshots/myaccount-page.png)

### Trip Details Page - Checklist

- Users can create and add a to-do list to the trip
- Users also have the option to mark a task as done or delete it

### Trip Details Page - Reservations

- Users can add reservations to the trip, including hotels, Airbnbs, Flight, Train, etc.
- Reservations are displayed as cards, and they can be deleted when you are done with them

### Trip Details Page - Activities

- Users can add activities to the trip. The categories are: Guided Tour, Arts & Culture, Outdoor Activities, etc.
- Activities are displayed as cards (which can also be deleted just like the reservations)

  ![Tripaholics - Trip Details](/static/screenshots/trip-details.gif)

### Trip Details Page - Invite a friend

- Users can invite a friend to join their trip by entering their email address. For this particular feature, I used SendGrid Mail API to send a personalized email invitation to the preferred email account.

  ![Tripaholics - Trip Details](/static/screenshots/invite-friend.png)

### 404 Error Page

- Included 404 error handler page just in case the page doesn't exist.

![Tripaholics - 404 Error Handler](/static/screenshots/404-error.png)

## Set Up

If you would like to run this project, here are the steps:

```
git clone https://github.com/rdpfeifle/Travel-web-app
```

Create and activate a virtual environment within your directory

```
python3 -m pip install --user virtualenv
source env/bin/activate
```

Install the dependencies:

```
pip3 install -r requirements.txt
```

Obtain keys for the Google Maps API, SendGrid API and Unsplash Images API

Save your Google Maps and Unsplash API keys in a file called `secrets.sh` using this format:

```
export YOUR_APP_KEY="YOUR_KEY_GOES_HERE"
```

Save your SendGrid API key in a file called `sendgrid.env` using this format:

```
export SENDGRID_API_KEY="YOUR_KEY_GOES_HERE"
```

Source your keys into your virtual environment:

```
source secrets.sh
source ./sendgrid.env
```

Set up the database:

```
python3 seed_database.py
```

Run the app:

```
python3 server.py
```

You can now navigate to 'localhost:5000/' to access the website

## About Me

👩🏻 Hi, my name is Raquel and I'm a Software Engineer. This travel web app was created in 4 weeks as my capstone project at Hackbright Academy, a 12-week accelerated Software Engineering fellowship. Feel free to connect on [LinkedIn](https://www.linkedin.com/in/raqueldpfeifle/)!
