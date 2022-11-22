# Tripaholics

## Table of Contents

- 🤖 [Technologies](#technologies-used)
- ⭐ [Features](#features)
- 🚀 [Future Improvements](#future-improvements)
- 📖 [Set Up](#set-up)
- 👩🏻 [About Me](#about-me)

## Technologies Used

- Front-end: Javascript, HTML5, CSS3, Bootstrap, AJAX, JSON
- Templating Engine: Jinja2
- Back-end: Python, Flask, PostgreSQL, SQLAlchemy
- APIs: Google Maps API, Twilio's SendGrid API, Unsplash Images API, Swiper API

## Features

### Homepage

- Homepage displays additional information about the project, including a navbar that automatically scrolls down when a link is clicked
- Users can click on the button to start planning, but they can create a trip only if they are logged in
- Users see recommended places to travel to in a beautiful carousel
- Users can read provided answers to a list of frequently asked questions about the project

### Sign up/Login

- Users can create an account and/or login
- Passwords are saved to the database already hashed for extra layer of security using Argon2

### More soon

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
