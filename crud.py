"""CRUD operations."""

from flask import session
from model import db, User, Animal, Favorite, Breed, ViewedAnimal, connect_to_db
import requests
import os
API_KEY = os.environ['PETFINDER_KEY']
API_SECRET = os.environ['PETFINDER_SECRET']


class local:
    token = ''

def create_user(first_name, last_name, email, password_hash, phone, address, city, state, zipcode):
    """Create and return a new user."""

    user = User(first_name=first_name, last_name=last_name, email=email, password_hash=password_hash, phone=phone,
    address=address, city=city, state=state, zipcode=zipcode)

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


def update_user_data(email, first_name, last_name, phone, address, city, state, zipcode):

    user = User.query.filter(User.email == email).first()
    if first_name is not None:
        user.first_name = first_name
        
    if last_name is not None:
        user.last_name = last_name
        
    if phone is not None:
        user.phone = phone
        
    if address is not None:
        user.address = address
        
    if city is not None:
        user.city = city
        
    if state is not None:
        user.state = state
        
    if zipcode is not None:
        user.zipcode = zipcode
        

    return user


def create_animal(animal_name):
    """Create and return a new animal."""
    animal = Animal(animal_name=animal_name)

    return animal


def get_animals():
    """Return all animals."""

    return Animal.query.all()


def create_favorite(user, animal_id, name, type, image, org_id):

    animal_id = int(animal_id)
    liked_animal = Animal().query.get(animal_id)
    if not liked_animal:
        liked_animal = Animal()
        liked_animal.animal_id = animal_id
        liked_animal.name = name
    db.session.add(liked_animal)
    favorite = Favorite().query.filter_by(user_id=user, animal_id=animal_id).first()
    if not favorite:
        favorite = Favorite(user_id=user, animal_id=animal_id, animal_name=name, animal_type=type, image=image, org_id=org_id)
        # favorite.user_id = user
        # favorite.animal_id = animal_id
        # favorite.animal_name = name
        # favorite.animal_type = type
        # favorite.image = image
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
    return response


def search_animals_by_breed(breed, location):
    """Send API request to get animals by the breed & zipcode."""
    
    headers = {
        'Authorization': 'Bearer ' + local.token,
    }
    
    res = requests.get(f'https://api.petfinder.com/v2/animals?breed={breed}&limit=100&location={location}&distance=100&sort=distance', headers=headers)    

    res = res.json()
    response = res['animals']
    return response


def get_animal_by_id(animal_id):
    """Get details of the animal by its id."""

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

def get_organizations(zipcode):
    """Get shelters/organizations near user's zipcode."""

    headers = {
    'Authorization': 'Bearer ' + local.token,
    }
    res = requests.get(f'https://api.petfinder.com/v2/organizations/?location={zipcode}&sort=distance', headers=headers)

    # If response came back with Error 401 due to expired token, renewing the token via POST request and sending the GET request again
    if res.status_code == 401:
        get_token()
        headers = {
            'Authorization': 'Bearer ' + local.token,
            }
        res = requests.get(f'https://api.petfinder.com/v2/organizations/?location={zipcode}&sort=distance', headers=headers)

    res = res.json()
    response = res['organizations']
    return response


def get_organization(org_id):
    """Get details of a shelter/organization by the organization id"""

    headers = {
    'Authorization': 'Bearer ' + local.token,
    }
    res = requests.get(f'https://api.petfinder.com/v2/organizations/{org_id}', headers=headers)

    # If response came back with Error 401 due to expired token, renewing the token via POST request and sending the GET request again
    if res.status_code == 401:
        get_token()
        headers = {
            'Authorization': 'Bearer ' + local.token,
            }
        res = requests.get(f'https://api.petfinder.com/v2/organizations/{org_id}', headers=headers)

    res = res.json()
    response = res['organization']
    return response


def get_animals_by_organization(org_id):
    """Get 9 animals available for adoption at specified shelter."""

    headers = {
    'Authorization': 'Bearer ' + local.token,
    }
    res = requests.get(f'https://api.petfinder.com/v2/animals?organizations={org_id}&limit=9', headers=headers)

    # If response came back with Error 401 due to expired token, renewing the token via POST request and sending the GET request again
    if res.status_code == 401:
        get_token()
        headers = {
            'Authorization': 'Bearer ' + local.token,
            }
        res = requests.get(f'https://api.petfinder.com/v2/animals?organizations={org_id}&limit=9', headers=headers)

    res = res.json()
    response = res['animals']
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


def get_bird_breeds():
    """Getting all bird breeds."""

    headers = {
    'Authorization': 'Bearer ' + local.token,
    }
    res = requests.get(f'https://api.petfinder.com/v2/types/bird/breeds', headers=headers)

    # If response came back with Error 401 due to expired token, renewing the token via POST request and sending the GET request again
    if res.status_code == 401:
        get_token()
        headers = {
            'Authorization': 'Bearer ' + local.token,
            }
        res = requests.get(f'https://api.petfinder.com/v2/types/bird/breeds', headers=headers)

    res = res.json()
    response = res['breeds']
    breeds = []
    for item in response:
        breeds.append(item['name'])
    return breeds
    

def create_breed(animal_type, breed_name):
    """Create and return a new breed."""

    breed = Breed(animal_type=animal_type, breed_name=breed_name)

    return breed


def get_breeds_by_animal_type(animal_type):
    """Return breeds by animal type."""

    breeds = Breed.query.filter(Breed.animal_type == animal_type).all()
    result = []
    for breed in breeds:
        result.append(breed.breed_name)
    return result


def create_viewed_animal(user_id, animal_id, name, type, image, org_id):
    """Track each viewed animal by particular user and add it to the database."""

    animal_id = int(animal_id)
    animal = Animal().query.get(animal_id)
    if not animal:
        animal = Animal(animal_id=animal_id, name=name)
        db.session.add(animal)
    viewed_animal = ViewedAnimal().query.filter_by(user_id=user_id, animal_id=animal_id).first()
    if not viewed_animal:
        viewed_animal = ViewedAnimal(user_id=user_id, animal_id=animal_id, animal_name=name, animal_type=type, image=image, org_id=org_id)
        db.session.add(viewed_animal)
    db.session.commit()

    return viewed_animal


def get_viewed_by_user_id(user_id):
    """Show last 6 animals user has viewed."""

    return ViewedAnimal.query.filter(ViewedAnimal.user_id == user_id)[-7:-1:]

if __name__ == '__main__':
    from server import app
    connect_to_db(app)