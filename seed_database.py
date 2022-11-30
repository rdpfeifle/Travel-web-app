"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime
from argon2 import PasswordHasher
ph = PasswordHasher()

import crud
import server
import model

model.connect_to_db(server.app)
model.db.create_all()
# from model import User, Trip, db, connect_to_db

os.system("dropdb trips")
os.system("createdb trips")


def fake_users():
    """Create fake users into database."""

    nick = crud.create_user(fname="Nick", lname="Whitlock", email="nick@gmail.com", password=ph.hash("123456"))
    amanda = crud.create_user(fname="Amanda", lname="Katz", email="amanda@gmail.com", password=ph.hash("1234")) 
    # raquel = crud.create_user(fname="Raquel", lname="Pfeifle", email="raquel@gmail.com", password=ph.hash("1234"))

    # model.db.session.add(nick)
    model.db.session.add_all([nick, amanda])
    model.db.session.commit()


# Load destinations data from JSON file
with open("data/destinations_imgs.json") as file:
    destinations_data = json.loads(file.read())

# Create trips, store them in a list so we 
# can use them to create fake destinations
imgs_in_db = []

for destination in destinations_data:
    city_name, place_name, description, url = (
        destination["city_name"],
        destination["place_name"],
        destination["description"],
        destination["url"],
    )

    db_images = crud.create_image(place_name, city_name, description, url)
    imgs_in_db.append(db_images)

model.db.session.add_all(imgs_in_db)
model.db.session.commit()


if __name__ == "__main__":

    fake_users()