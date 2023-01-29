"""Server for pet shelter website."""

from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db
import crud, os, requests
from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = 'dev'
API_KEY = os.environ['PETFINDER_KEY']
API_SECRET = os.environ['PETFINDER_SECRET']
GEO_API = os.environ['GEOCODING_API']
GOOGLE_MAPS_KEY = os.environ['GOOGLE_MAPS_KEY']
GOOGLE_GEOCODING_KEY = os.environ['GOOGLE_GEOCODING_KEY']
app.jinja_env.undefined = StrictUndefined



@app.route('/')
def homepage():
    """View homepage."""

    # API request for user's geolocation in case user profile doesn't have zipcode saved.
    response = requests.get("http://ip-api.com/json/")
    response = response.json()
    zip = response['zip']
    # Saving user's zipcode in the session
    session["zipcode"] = zip

    # Sending Petfinder POST API request to get API access token.
    crud.get_token()
    # Querying for breed options from Petfinder
    dog_breeds_db = crud.get_breeds_by_animal_type("dog")
    cat_breeds_db = crud.get_breeds_by_animal_type("cat")
    rabbit_breeds_db = crud.get_breeds_by_animal_type("rabbit")
    bird_breeds_db = crud.get_breeds_by_animal_type("bird")

    # Querying the database for recently viewed animals by a particular user
    logged_in_email = session.get("user_email")
    if not logged_in_email:
        recently_viewed = []
    else:
        user_id = crud.get_user_by_email(logged_in_email).user_id
        recently_viewed = crud.get_viewed_by_user_id(user_id)

    return render_template('homepage.html', dog_breeds=dog_breeds_db, cat_breeds=cat_breeds_db, rabbit_breeds=rabbit_breeds_db, bird_breeds=bird_breeds_db, recently_viewed_animals=recently_viewed)


@app.route('/', methods=["POST"])
def search_with_keyword():
    # Sending CRUD request for a specific breed and zipcode user entered
    breed = request.form.get('breed')
    location = request.form.get('location')
    animals = crud.search_animals_by_breed(breed, location)
    
    return render_template('animals.html', animals=animals)


@app.route('/animals/<animal_type>')
def show_animals(animal_type):
    """Get a view of selected category of animals available for adoption."""
    #  Grabbing user's zipcode
    logged_in_email = session.get("user_email")
    if logged_in_email is None:
        zipcode = session.get('zipcode')
    else:
        user = crud.get_user_by_email(logged_in_email)
        if user.zipcode == None:
            zipcode = session.get('zipcode')
        else:
            zipcode = user.zipcode
    # Sending CRUD request to show animals near user's location
    animals=crud.get_animals_view(animal_type, zipcode=zipcode)
    
    return render_template('animals.html', animals=animals)


@app.route('/dog/<org_id>/<animal_id>')
def show_dog_details(org_id, animal_id):
    """View detailed information about the dog with specific id."""
    # HTML page title
    context = {
        'title': "Adoptable Dog"
    }

    animal=crud.get_animal_by_id(animal_id)

    # Storing viewed animal in the database
    logged_in_email = session.get("user_email")
    if not logged_in_email:
        recently_viewed = []
    else:
        user_id = crud.get_user_by_email(logged_in_email).user_id
        name = animal.get('name')
        org_id = animal.get('organization_id')
        type = (animal.get('type')).lower()
        breed = animal['breeds']['primary']
        if animal.get('primary_photo_cropped'):
            photos = animal.get('primary_photo_cropped')
            image = photos.get('small')
        else:
            image = "/static/img/dog_placeholder.jpeg"
            
        viewed_animal = crud.create_viewed_animal(user_id, animal_id, name, type, breed, image, org_id)
        recently_viewed = crud.get_viewed_by_user_id(user_id)

    return render_template('animal_details.html', context=context, animal=animal, recently_viewed_animals=recently_viewed, google_maps_api_key=GOOGLE_MAPS_KEY, google_geo_key=GOOGLE_GEOCODING_KEY)


@app.route('/cat/<org_id>/<animal_id>')
def show_cat_details(org_id, animal_id):
    """View detailed information about the cat with specific id."""
    # HTML page title
    context = {
        'title': "Adoptable Cat"
    }

    animal=crud.get_animal_by_id(animal_id)

    # Storing viewed animal in the database
    logged_in_email = session.get("user_email")
    if not logged_in_email:
        recently_viewed = []
    else:
        user_id = crud.get_user_by_email(logged_in_email).user_id
        name = animal.get('name')
        org_id = animal.get('organization_id')
        type = (animal.get('type')).lower()
        breed = animal['breeds']['primary']
        if animal.get('primary_photo_cropped'):
            photos = animal.get('primary_photo_cropped')
            image = photos.get('small')
        else:
            image = "/static/img/cat_placeholder.jpeg"

        viewed_animal = crud.create_viewed_animal(user_id, animal_id, name, type, breed, image, org_id)
        recently_viewed = crud.get_viewed_by_user_id(user_id)

    return render_template('animal_details.html', context=context, animal=animal, recently_viewed_animals=recently_viewed, google_maps_api_key=GOOGLE_MAPS_KEY, google_geo_key=GOOGLE_GEOCODING_KEY)


@app.route('/rabbit/<org_id>/<animal_id>')
def show_rabbit_details(org_id, animal_id):
    """View detailed information about the rabbit with specific id."""
    # HTML page title
    context = {
        'title': "Adoptable Rabbit"
    }

    animal=crud.get_animal_by_id(animal_id)

    # Storing viewed animal in the database
    logged_in_email = session.get("user_email")
    if not logged_in_email:
        recently_viewed = []
    else:
        user_id = crud.get_user_by_email(logged_in_email).user_id
        name = animal.get('name')
        org_id = animal.get('organization_id')
        type = (animal.get('type')).lower()
        breed = animal['breeds']['primary']
        if animal.get('primary_photo_cropped'):
            photos = animal.get('primary_photo_cropped')
            image = photos.get('small')
        else:
            image = "/static/img/rabbit_placeholder.jpeg"

        viewed_animal = crud.create_viewed_animal(user_id, animal_id, name, type, breed, image, org_id)
        recently_viewed = crud.get_viewed_by_user_id(user_id)

    return render_template('animal_details.html', context=context, animal=animal, recently_viewed_animals=recently_viewed, google_maps_api_key=GOOGLE_MAPS_KEY, google_geo_key=GOOGLE_GEOCODING_KEY)


@app.route('/bird/<org_id>/<animal_id>')
def show_bird_details(org_id, animal_id):
    """View detailed information about the bird with specific id."""
    # HTML page title
    context = {
        'title': "Adoptable Bird"
    }

    animal=crud.get_animal_by_id(animal_id)

    # Storing viewed animal in the database
    logged_in_email = session.get("user_email")
    if not logged_in_email:
        recently_viewed = []
    else:
        user_id = crud.get_user_by_email(logged_in_email).user_id
        name = animal.get('name')
        org_id = animal.get('organization_id')
        type = (animal.get('type')).lower()
        breed = animal['breeds']['primary']
        if animal.get('primary_photo_cropped'):
            photos = animal.get('primary_photo_cropped')
            image = photos.get('small')
        else:
            image = "/static/img/bird_placeholder.jpeg"

        viewed_animal = crud.create_viewed_animal(user_id, animal_id, name, type, breed, image, org_id)
        recently_viewed = crud.get_viewed_by_user_id(user_id)

    return render_template('animal_details.html', context=context, animal=animal, recently_viewed_animals=recently_viewed, google_maps_api_key=GOOGLE_MAPS_KEY, google_geo_key=GOOGLE_GEOCODING_KEY)


@app.route('/view/organizations')
def show_organizations():
    """Get a view of organizations nearby."""

    logged_in_email = session.get("user_email")

    if logged_in_email is None:
        zipcode = session.get('zipcode')
    else:
        user = crud.get_user_by_email(logged_in_email)
        if user.zipcode == None:
            zipcode = session.get('zipcode')
        else:
            zipcode = user.zipcode

    organizations=crud.get_organizations(zipcode=zipcode)
    
    return render_template('organizations.html', organizations=organizations)


@app.route('/view/organizations/<org_id>')
def show_organization_details(org_id):
    """Show details of selected organization."""

    organization = crud.get_organization(org_id)
    animals = crud.get_animals_by_organization(org_id)

    return render_template('organization_details.html', organization=organization, animals=animals, google_maps_api_key=GOOGLE_MAPS_KEY, google_geo_key=GOOGLE_GEOCODING_KEY)


@app.route('/favorite/<animal_id>')
def favorite_animal(animal_id):
    """Add the animal to favorites list"""

    logged_in_email = session.get("user_email")

    if logged_in_email is None:
        flash("Create or sign in to your account to add this pet to your favorites.", 'warning')
        return redirect(request.referrer)
    else:
        user_id = crud.get_user_by_email(logged_in_email).user_id
        animal = crud.get_animal_by_id(animal_id)
        name = animal.get('name')
        org_id = animal.get('organization_id')
        type = (animal.get('type')).lower()
        if animal.get('primary_photo_cropped'):
            photos = animal.get('primary_photo_cropped')
            image = photos.get('small')
        else:
            if animal.get('type') == 'Dog':
                image = "/static/img/dog_placeholder.jpeg"
            elif animal.get('type') == 'Cat':
                image = "/static/img/cat_placeholder.jpeg"
            elif animal.get('type') == "Rabbit":
                image = "/static/img/rabbit_placeholder.jpeg"
            elif animal.get('type') == "Bird":
                image = "/static/img/bird_placeholder.jpeg"
        favorite = crud.create_favorite(user_id, animal_id, name, type, image, org_id)
        flash(f"{name} has been added to favorites list.", 'success')
    
    return redirect(request.referrer)


@app.route('/unfavorite/<animal_id>')
def unfavorite_animal(animal_id):
    """Remove the animal from favorites list."""

    logged_in_email = session.get("user_email")

    if logged_in_email is None:
        flash("Create or sign in to your account to add this pet to your favorites.", 'warning')
        return redirect(request.referrer)
    else:
        user_id = crud.get_user_by_email(logged_in_email).user_id
        animal = crud.get_animal_by_id(animal_id)
        animal_id = animal.get('id')
        crud.delete_favorite(user_id=user_id, animal_id=animal_id)
        flash(f"{animal.get('name')} has been removed from your favorites list.", 'success')
    
    return redirect('/favorites')


@app.route('/user')
def show_user():
    """Show user's profile page."""

    logged_in_email = session.get("user_email")
    if logged_in_email is None:
        flash("Please log in to your account.", 'warning')
        return redirect('/')
    
    user = crud.get_user_by_email(logged_in_email)

    return render_template('user_profile.html', user=user)


@app.route('/register', methods=["POST"])
def register_user():
    """Create a new user account."""

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)

    if user:
        flash("User with this email already exists. Please create account with a different email.", 'warning')
    else:
        user = crud.create_user(first_name=first_name, last_name=last_name, email=email, password_hash=password, phone=None, address=None, city=None, state=None, zipcode=None)
        db.session.add(user)
        db.session.commit()
        flash("New account has been created. Please log in using your credentials.", 'success')
        
    return redirect('/')


@app.route('/login', methods=["POST"])
def handle_login():
    """Process a user login."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if not user:
        flash("Account with this email doesn't exist. Please try again.", 'warning')
    elif user.password_hash != password:
        flash("Password you have entered is incorrect. Please try again.", 'warning')
    else:
        session["user_email"] = user.email
        flash(f"Welcome back, {user.first_name}!", 'success')

    return redirect(request.referrer)


@app.route('/logout')
def handle_logout():
    """Log the user out."""

    del session["user_email"]
    del session["zipcode"]
    flash("You have logged out successfully!", 'success')
    return redirect('/')


@app.route('/favorites')
def show_favorites():
    """Display user's favorited pets."""

    logged_in_email = session.get("user_email")

    if logged_in_email is None:
        flash("Create or sign in to your account to view favorite pets.", 'warning')
        return redirect('/')
    else:
        user_id = crud.get_user_by_email(logged_in_email).user_id

    return render_template("favorites.html", favorites=crud.get_favorites_by_user_id(user_id))


@app.route('/user/update/form', methods=["POST"])
def update_user_profile():
    """Update user details."""

    first_name = request.form.get('first-name', None)
    last_name = request.form.get('last-name', None)
    phone = request.form.get('phone', None)
    address = request.form.get('street', None)
    city = request.form.get('city', None)
    state = request.form.get('state', None)
    zipcode = request.form.get('zip', None)
    email = session.get('user_email', None)
    if not email:
        flash("Please log in or create an account!", 'warning')
        return redirect("/")
    
    user = crud.update_user_data(email, first_name, last_name, phone, address, city, state, zipcode)
    db.session.commit()
    
    flash("Your profile has been updated.", 'success')

    return redirect(f'/user')
    

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)