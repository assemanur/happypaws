"""Script to seed database."""

import os
import json
from random import choice
from datetime import datetime

import crud
import model
import server

os.system('dropdb pet-shelter')
os.system('createdb pet_shelter')

model.connect_to_db(server.app)
model.db.create_all()

#Inserting fake users data into the database
with open('data/users_mock_data.json') as f:
    users_data = json.loads(f.read())

#Iterating through each item in dictionary
users_in_db = []
for user in users_data:
    first_name, last_name, email, password_hash, phone, address, city, state, zipcode = (
        user["first_name"],
        user["last_name"],
        user["email"],
        user["password_hash"],
        user["phone"],
        user["address"],
        user["city"],
        user["state"],
        user["zipcode"],
    )
    created_at = datetime.strptime(user["created_at"], "%m/%d/%Y")

    db_users = crud.create_user(first_name, last_name, email, password_hash, phone, address, city, state, zipcode, created_at)
    users_in_db.append(db_users)

model.db.session.add_all(users_in_db)

#Inserting fake animals data into animals table
# with open('data/animals_data.json') as l:
#     animals_data = json.loads(l.read())

# animals_in_db = []

# for animal in animals_data:
#     name = animal["animal_name"]
#     db_animals = crud.create_animal(name)
#     animals_in_db.append(db_animals)

# model.db.session.add_all(animals_in_db)

#Inserting sample favorites into favorites table
# for n in range(100):
#     random_user = choice(users_in_db)
#     random_animal = choice(animals_in_db)

#     favorite = crud.create_favorite(random_user, random_animal)
#     model.db.session.add(favorite)

dog_breeds = crud.get_dog_breeds()
cat_breeds = crud.get_cat_breeds()
rabbit_breeds = crud.get_rabbit_breeds()
bird_breeds = crud.get_bird_breeds()

breeds_in_db = []
for breed in dog_breeds:
    db_breed = crud.create_breed(animal_type="dog", breed_name=breed)
    breeds_in_db.append(db_breed)

for breed in cat_breeds:
    db_breed = crud.create_breed(animal_type="cat", breed_name=breed)
    breeds_in_db.append(db_breed)

for breed in rabbit_breeds:
    db_breed = crud.create_breed(animal_type="rabbit", breed_name=breed)
    breeds_in_db.append(db_breed)

for breed in bird_breeds:
    db_breed = crud.create_breed(animal_type="bird", breed_name=breed)
    breeds_in_db.append(db_breed)

model.db.session.add_all(breeds_in_db)
model.db.session.commit()