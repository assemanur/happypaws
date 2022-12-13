"""CRUD operations."""

from model import db, User, Animal, Favorite, connect_to_db
from datetime import datetime

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

def create_animal(animal_name):
    """Create and return a new animal."""
    animal = Animal(animal_name=animal_name)

    return animal


def get_animals():
    """Return all animals."""

    return Animal.query.all()


def get_animal_by_id(animal_id):
    """Return an animal by primary key."""

    return Animal.query.get(animal_id)


def create_favorite(user, animal):
    """Create and return favorite pet."""

    favorite = Favorite(user=user, animal=animal)
    return favorite


if __name__ == '__main__':
    from server import app
    connect_to_db(app)