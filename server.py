"""Server for pet shelter website."""

from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db
import crud
from datetime import datetime

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')


@app.route('/animals')
def all_animals():
    """View all animals list."""

    animals = crud.get_animals()

    return render_template('all_animals.html', animals=animals)


@app.route('/animals/<animal_id>')
def show_animal(animal_id):
    """Show details of a particular animal."""

    animal = crud.get_animal_by_id(animal_id)

    return render_template('animal_details.html', animal=animal)


@app.route('/users')
def all_users():
    """View all users list."""

    users = crud.get_users()

    return render_template('all_users.html', users=users)


@app.route('/users/<user_id>')
def show_user(user_id):
    """Show info of a particular user."""

    user = crud.get_animal_by_id(user_id)

    return render_template('user_details.html', user=user)


@app.route('/users', methods=["POST"])
def register_user():
    """Create a new user account."""

    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)

    if user:
        flash("User with this email already exists. Please create account with a different email.")
    else:
        user = crud.create_user(first_name=None, last_name=None, email=email, password_hash=password, phone=None, address=None, city=None, state=None, zipcode=None, created_at=None)
        db.session.add(user)
        db.session.commit()
        flash("New account has been created. Please log in using your credentials.")
        
    return redirect('/')


@app.route('/login', methods=["POST"])
def handle_login():
    """Process a user login."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if not user:
        flash("Account with this email doesn't exist. Please try again.")
    elif user.password_hash != password:
        flash("Password you have entered is incorrect.Please try again.")
    else:
        session["user_email"] = user.email
        flash(f"Welcome back, {user.email}!")
    
    return redirect('/')




if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)