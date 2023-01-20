"""Models for pet shelter app."""

from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """A user"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String, nullable=True)
    last_name = db.Column(db.String, nullable=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=True)
    address = db.Column(db.String, nullable=True)
    city = db.Column(db.String, nullable=True)
    state = db.Column(db.String, nullable=True)
    zipcode = db.Column(db.Integer, nullable=True)

    favorites = db.relationship("Favorite", back_populates="user")
    viewed = db.relationship("ViewedAnimal", back_populates="user")

    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"


class Animal(db.Model):
    """Create and return an animal."""

    __tablename__ = "animals"

    animal_id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    name = db.Column(db.String, nullable=False)

    favorites = db.relationship("Favorite", back_populates="animal")
    viewed = db.relationship("ViewedAnimal", back_populates="animal")

    def __repr__(self):

        return f"<Animal animal_id={self.animal_id} animal_name={self.animal_name}>"


class Shelter(db.Model):
    """Information about shelter."""

    __tablename__ = "shelter"

    shelter_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    zipcode = db.Column(db.String)

    def __repr__(self):

        return f"<Shelter shelter_id={self.shelter_id} shelter_name={self.name}>"


class Favorite(db.Model):
    """Favorite pet"""

    __tablename__ = "favorites"

    # __table_args__= (db.UniqueConstraint('user_id', 'animal_id'), )

    fav_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    animal_id = db.Column(db.Integer, db.ForeignKey("animals.animal_id"))
    animal_name = db.Column(db.String)
    animal_type = db.Column(db.String(10))
    image = db.Column(db.String(200), nullable=True)
    org_id = db.Column(db.String)

    user = db.relationship("User", back_populates="favorites")
    animal = db.relationship("Animal", back_populates="favorites")

    def __repr__(self):
        return f"<Favorite fav_id={self.fav_id} animal_id={self.animal_id}>"

    

class Breed(db.Model):
    """Adding animals breeds to the database."""

    __tablename__ = "breeds"

    breed_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    animal_type = db.Column(db.String)
    breed_name = db.Column(db.String)

    def __repr__(self):
        return f"<Breed animal_type={self.animal_type} breed_name={self.breed_name}>"


class ViewedAnimal(db.Model):

    __tablename__ = "viewed_animals"

    view_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    animal_id = db.Column(db.Integer, db.ForeignKey("animals.animal_id"))
    animal_name = db.Column(db.String)
    animal_type = db.Column(db.String(10))
    breed = db.Column(db.String)
    image = db.Column(db.String(200), nullable=True)
    org_id = db.Column(db.String)

    user = db.relationship("User", back_populates="viewed")
    animal = db.relationship("Animal", back_populates="viewed")

    def __repr__(self):
        return f"<Viewed by user_id={self.user_id} animal_id={self.animal_id}>"
    


def connect_to_db(flask_app, db_uri="postgresql:///pet_shelter", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)