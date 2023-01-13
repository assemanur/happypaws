"""CRUD operations."""

from flask import session
from model import db, User, Animal, Favorite, connect_to_db
from datetime import datetime
import requests
import os
API_KEY = os.environ['PETFINDER_KEY']
API_SECRET = os.environ['PETFINDER_SECRET']


class local:
    token = ''

def create_user(first_name, last_name, email, password_hash, phone, address, city, state, zipcode, created_at):
    """Create and return a new user."""

    user = User(first_name=first_name, last_name=last_name, email=email, password_hash=password_hash, phone=phone, address=address, city=city, state=state, zipcode=zipcode, created_at=created_at)

    return user


def get_users():
    """Return all users."""

    return User.query.all()


def get_user_by_id(user_id):
    """Return a user by primary key."""

    return User.query.get(user_id)


def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()


def get_user_id_only(email):

    user = User.query.filter(User.email == email).first()
    return user.pk
    

def update_zipcode(email, zipcode):
    """Update user's zipcode."""
    user = User.query.filter(User.email == email).first()
    user.zipcode = zipcode

    return user


def create_animal(animal_name):
    """Create and return a new animal."""
    animal = Animal(animal_name=animal_name)

    return animal


def get_animals():
    """Return all animals."""

    return Animal.query.all()


def create_favorite(user, animal_id, name, type, image):

    animal_id = int(animal_id)
    liked_animal = Animal().query.get(animal_id)
    if not liked_animal:
        liked_animal = Animal()
        liked_animal.animal_id = animal_id
        liked_animal.name = name
    db.session.add(liked_animal)
    favorite = Favorite().query.filter_by(user_id=user, animal_id=animal_id).first()
    if not favorite:
        favorite = Favorite()
        favorite.user_id = user
        favorite.animal_id = animal_id
        favorite.animal_name = name
        favorite.animal_type = type
        favorite.image = image
    db.session.add(favorite)
    db.session.commit()
    return favorite


def delete_favorite(user_id, animal_id):
    """Remove a record from favorite table for a specific animal by a specified user"""
    animal_id = int(animal_id)
    unfavorite = Favorite().query.filter_by(user_id=user_id, animal_id=animal_id).first()
    db.session.delete(unfavorite)
    db.session.commit()
    return



def get_favorite():

    return Favorite.query.all()


def get_favorites_by_user_id(user_id):

    return Favorite.query.filter(Favorite.user_id == user_id).all()


def get_token():
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = f'grant_type=client_credentials&client_id={API_KEY}&client_secret={API_SECRET}'

    res = requests.post('https://api.petfinder.com/v2/oauth2/token', headers=headers, data=data)
    response = res.json()
    local.token = response['access_token']
    return local.token


def get_animals_view(animal_type, zipcode=None):

    headers = {
        'Authorization': 'Bearer ' + local.token,
    }
    # If user's zipcode is known, sending GET request to show animals within 50 miles from user's location
    if zipcode:
        res = requests.get(f'https://api.petfinder.com/v2/animals?type={animal_type}&limit=100&location={zipcode}&distance=50&sort=distance', headers=headers)
        # If response came back with Error 401 due to expired token, renewing the token via POST request and sending the GET request again
        if res.status_code == 401:
            get_token()
            headers = {
                'Authorization': 'Bearer ' + local.token,
            }
            res = requests.get(f'https://api.petfinder.com/v2/animals?type={animal_type}&limit=100&location={zipcode}&distance=50&sort=distance', headers=headers)
    
    # If user's zipcode is unknown and there is no zipcode stored in session, then show random animals available for adoption
    else:
        res = requests.get(f'https://api.petfinder.com/v2/animals?type={animal_type}&limit=100', headers=headers)
        # If response came back with Error 401 due to expired token, renewing the token via POST request and sending the GET request again
        if res.status_code == 401:
            get_token()
            headers = {
                'Authorization': 'Bearer ' + local.token,
            }
            res = requests.get(f'https://api.petfinder.com/v2/animals?type={animal_type}&limit=100', headers=headers)
    
    res = res.json()
    response = res['animals']
    # print(response)
    return response

    # headers = {
    #     'Authorization': 'Bearer ' + local.token,
    # }
    # if zipcode:
    #     res = requests.get(f'https://api.petfinder.com/v2/animals?type={animal_type}&limit=100&location={zipcode}&distance=50&sort=distance', headers=headers)
    
    # else:
    #     res = requests.get(f'https://api.petfinder.com/v2/animals?type={animal_type}&limit=100', headers=headers)
    
    # res = res.json()
    # response = res['animals']
    # return response


def search_animals_with_keyword(string, location):
    headers = {
        'Authorization': 'Bearer ' + local.token,
    }
    res = requests.get(f'https://api.petfinder.com/v2/types/{type}/breeds')
    res = requests.get(f'https://api.petfinder.com/v2/animals?type={animal_type}&limit=100&location={zipcode}&distance=50&sort=distance', headers=headers)    

    # if zipcode:
        # filtered_res = list()
        # for animal in res:
        #     print(f"{int(animal['contact']['address']['postcode'])}-{int(zipcode)}")
        #     if  int(animal['contact']['address']['postcode'])==int(zipcode):
        #         print(animal)
        #         filtered_res.append(animal)
        # res = filtered_res.copy()
        # res = list(filter(lambda item: (int(item['contact']['address']['postcode'])==int(zipcode)), res))


def get_animal_by_id(animal_id):

    headers = {
    'Authorization': 'Bearer ' + local.token,
    }
    res = requests.get(f'https://api.petfinder.com/v2/animals/{animal_id}', headers=headers)
    # If response came back with Error 401 due to expired token, renewing the token via POST request and sending the GET request again
    if res.status_code == 401:
        get_token()
        headers = {
            'Authorization': 'Bearer ' + local.token,
            }
        res = requests.get(f'https://api.petfinder.com/v2/animals/{animal_id}', headers=headers)

    res = res.json()
    response = res['animal']

    return response


def add_shelter(shelter_id):

    headers = {
    'Authorization': 'Bearer ' + local.token,
    }
    res = requests.get(f'https://api.petfinder.com/v2/organizations/{shelter_id}', headers=headers)

    # If response came back with Error 401 due to expired token, renewing the token via POST request and sending the GET request again
    if res.status_code == 401:
        get_token()
        headers = {
            'Authorization': 'Bearer ' + local.token,
            }
        res = requests.get(f'https://api.petfinder.com/v2/organizations/{shelter_id}', headers=headers)

    res = res.json()
    response = res['organization']
    return response


def get_dog_breeds():
    """Getting all dog breeds."""

    headers = {
    'Authorization': 'Bearer ' + local.token,
    }
    res = requests.get(f'https://api.petfinder.com/v2/types/dog/breeds', headers=headers)

    # If response came back with Error 401 due to expired token, renewing the token via POST request and sending the GET request again
    if res.status_code == 401:
        get_token()
        headers = {
            'Authorization': 'Bearer ' + local.token,
            }
        res = requests.get(f'https://api.petfinder.com/v2/types/dog/breeds', headers=headers)

    res = res.json()
    response = res['breeds']
    breeds = []
    for item in response:
        breeds.append(item['name'])
    return breeds
    

def get_cat_breeds():
    """Getting all cat breeds."""

    headers = {
    'Authorization': 'Bearer ' + local.token,
    }
    res = requests.get(f'https://api.petfinder.com/v2/types/cat/breeds', headers=headers)

    # If response came back with Error 401 due to expired token, renewing the token via POST request and sending the GET request again
    if res.status_code == 401:
        get_token()
        headers = {
            'Authorization': 'Bearer ' + local.token,
            }
        res = requests.get(f'https://api.petfinder.com/v2/types/cat/breeds', headers=headers)

    res = res.json()
    response = res['breeds']
    breeds = []
    for item in response:
        breeds.append(item['name'])
    return breeds


def get_rabbit_breeds():
    """Getting all rabbit breeds."""

    headers = {
    'Authorization': 'Bearer ' + local.token,
    }
    res = requests.get(f'https://api.petfinder.com/v2/types/rabbit/breeds', headers=headers)

    # If response came back with Error 401 due to expired token, renewing the token via POST request and sending the GET request again
    if res.status_code == 401:
        get_token()
        headers = {
            'Authorization': 'Bearer ' + local.token,
            }
        res = requests.get(f'https://api.petfinder.com/v2/types/rabbit/breeds', headers=headers)

    res = res.json()
    response = res['breeds']
    breeds = []
    for item in response:
        breeds.append(item['name'])
    return breeds
    

def get_geocode():
    return

    # headers = {
    # 'Authorization': 'Bearer ' + local.token,
    # }
    # res = requests.get(f'https://api.petfinder.com/v2/animals/{animal_id}', headers=headers)
    # res = res.json()
    
    # response = res['animal']
    # return response



if __name__ == '__main__':
    from server import app
    connect_to_db(app)