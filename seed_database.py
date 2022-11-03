"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime
from passlib.hash import argon2
import crud

from model import User, Trip, db, connect_to_db
import server

os.system("dropdb trips")
os.system("createdb trips")

connect_to_db(server.app)
db.create_all()

def fake_users():
    """Create fake users into database."""

    nick = crud.create_user(fname="Nick", lname="Whitlock", email="nick@gmail.com", password=argon.hash("123456"))

    db.session.add(nick)
    db.session.commit()

# create fake trips below
# def fake_trips():


# Load destinations data from JSON file
with open("data/destinations_imgs.json") as file:
    destinations_data = json.loads(file.read())

# Create trips, store them in a list so we 
# can use them to create fake ratings
destinations_imgs_in_db = []

for destination in destinations_data:
    city_name, place_name, description, url = (
        destination["city_name"],
        destination["place_name"],
        destination["description"],
        destination["url"],
    )

    #still need to create function in crud.py for the images
    # maybe i will call image_displays() #it will just display at the homepage
    db_images = crud.image_displays(city_name, place_name, description, url)
    destinations_imgs_in_db.append(db_images)

db.session.add_all(destinations_imgs_in_db)
db.session.commit()

if __name__ == "__main__":
    os.system('dropdb trips')
    os.system('createdb trips')

    connect_to_db(app)
    db.create_all()

    fake_users()
    # fake_trips()