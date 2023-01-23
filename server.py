"""Server for pet shelter website."""

from flask import (Flask, render_template, request, flash, session, redirect, jsonify)
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

    # API request for user's geolocation in case if user profile doesn't have zipcode saved.
    response = requests.get("http://ip-api.com/json/")
    response = response.json()
    zip = response['zip']
    print(zip)
    session["zipcode"] = zip

    #Sending Petfinder API request to get API token.
    crud.get_token()
    
    dog_breeds_db = crud.get_breeds_by_animal_type("dog")
    cat_breeds_db = crud.get_breeds_by_animal_type("cat")
    rabbit_breeds_db = crud.get_breeds_by_animal_type("rabbit")
    bird_breeds_db = crud.get_breeds_by_animal_type("bird")

    logged_in_email = session.get("user_email")
    if not logged_in_email:
        recently_viewed = []
    else:
        user_id = crud.get_user_by_email(logged_in_email).user_id
        recently_viewed = crud.get_viewed_by_user_id(user_id)

    return render_template('homepage.html', dog_breeds=dog_breeds_db, cat_breeds=cat_breeds_db, rabbit_breeds=rabbit_breeds_db, bird_breeds=bird_breeds_db, recently_viewed_animals=recently_viewed)


@app.route('/', methods=["POST"])
def search_with_keyword():

    breed = request.form.get('breed')
    location = request.form.get('location')
    print(f"\033[36m█▓▒░ | Search form has been submitted \033[0m")
    animals = crud.search_animals_by_breed(breed, location)
    
    return render_template('animals.html', animals=animals)


@app.route('/animals/<animal_type>')
def show_animals(animal_type):
    """Get a view of selected category of animals available for adoption."""

    logged_in_email = session.get("user_email")
    if logged_in_email is None:
        zipcode = session.get('zipcode')
    else:
        user = crud.get_user_by_email(logged_in_email)
        if user.zipcode == None:
            zipcode = session.get('zipcode')
        else:
            zipcode = user.zipcode

    animals=crud.get_animals_view(animal_type, zipcode=zipcode)
    
    return render_template('animals.html', animals=animals)


@app.route('/dog/<org_id>/<animal_id>')
def show_dog_details(org_id, animal_id):
    """View detailed information about the dog with specific id."""

    context = {
        'title': "Adoptable Dog",
        'header': 'Adopt a Dog'
    }

    animal=crud.get_animal_by_id(animal_id)

    # Storing viewed animal to the database
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
            if animal.get('type') == 'Dog':
                image = "https://media.istockphoto.com/id/942318196/vector/dog-puppy-smiling-funny-animals-coloring-pages-cartoon-vector-illustration.jpg?s=612x612&w=0&k=20&c=VmV1zfZ56Kulm6nbf3wzeZfef3DwIHpT22lt4dK52nA="
            elif animal.get('type') == 'Cat':
                image = "https://i.etsystatic.com/7867651/r/il/929251/1234114682/il_1588xN.1234114682_1t12.jpg"
            elif animal.get('type') == "Rabbit":
                image = "https://i.etsystatic.com/21185388/r/il/dc90fa/2226677215/il_1588xN.2226677215_6bov.jpg"
            elif animal.get('type') == "Bird":
                image = "https://i.etsystatic.com/33889596/r/il/1e530a/3744462889/il_1588xN.3744462889_4k4v.jpg"
        viewed_animal = crud.create_viewed_animal(user_id, animal_id, name, type, breed, image, org_id)
        recently_viewed = crud.get_viewed_by_user_id(user_id)
        print(f"\033[35m█▓▒░ | {name} has been added to viewed_animals table \033[0m")

    return render_template('animal_details.html', context=context, animal=animal, recently_viewed_animals=recently_viewed, google_maps_api_key=GOOGLE_MAPS_KEY, google_geo_key=GOOGLE_GEOCODING_KEY)


@app.route('/cat/<org_id>/<animal_id>')
def show_cat_details(org_id, animal_id):
    """View detailed information about the cat with specific id."""
    
    context = {
        'title': "Adoptable Cat",
        'header': 'Adopt a Cat'
    }

    animal=crud.get_animal_by_id(animal_id)

    # Storing viewed animal to the database
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
            if animal.get('type') == 'Dog':
                image = "https://media.istockphoto.com/id/942318196/vector/dog-puppy-smiling-funny-animals-coloring-pages-cartoon-vector-illustration.jpg?s=612x612&w=0&k=20&c=VmV1zfZ56Kulm6nbf3wzeZfef3DwIHpT22lt4dK52nA="
            elif animal.get('type') == 'Cat':
                image = "https://i.etsystatic.com/7867651/r/il/929251/1234114682/il_1588xN.1234114682_1t12.jpg"
            elif animal.get('type') == "Rabbit":
                image = "https://i.etsystatic.com/21185388/r/il/dc90fa/2226677215/il_1588xN.2226677215_6bov.jpg"
            elif animal.get('type') == "Bird":
                image = "https://i.etsystatic.com/33889596/r/il/1e530a/3744462889/il_1588xN.3744462889_4k4v.jpg"
        viewed_animal = crud.create_viewed_animal(user_id, animal_id, name, type, breed, image, org_id)
        recently_viewed = crud.get_viewed_by_user_id(user_id)
        print(f"\033[35m█▓▒░ | {name} has been added to viewed_animals table \033[0m")

    return render_template('animal_details.html', context=context, animal=animal, recently_viewed_animals=recently_viewed, google_maps_api_key=GOOGLE_MAPS_KEY, google_geo_key=GOOGLE_GEOCODING_KEY)


@app.route('/rabbit/<org_id>/<animal_id>')
def show_rabbit_details(org_id, animal_id):
    """View detailed information about the rabbit with specific id."""
    
    context = {
        'title': "Adoptable Rabbit",
        'header': 'Adopt a Rabbit'
    }

    animal=crud.get_animal_by_id(animal_id)

    # Storing viewed animal to the database
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
            if animal.get('type') == 'Dog':
                image = "https://media.istockphoto.com/id/942318196/vector/dog-puppy-smiling-funny-animals-coloring-pages-cartoon-vector-illustration.jpg?s=612x612&w=0&k=20&c=VmV1zfZ56Kulm6nbf3wzeZfef3DwIHpT22lt4dK52nA="
            elif animal.get('type') == 'Cat':
                image = "https://i.etsystatic.com/7867651/r/il/929251/1234114682/il_1588xN.1234114682_1t12.jpg"
            elif animal.get('type') == "Rabbit":
                image = "https://i.etsystatic.com/21185388/r/il/dc90fa/2226677215/il_1588xN.2226677215_6bov.jpg"
            elif animal.get('type') == "Bird":
                image = "https://i.etsystatic.com/33889596/r/il/1e530a/3744462889/il_1588xN.3744462889_4k4v.jpg"
        viewed_animal = crud.create_viewed_animal(user_id, animal_id, name, type, breed, image, org_id)
        recently_viewed = crud.get_viewed_by_user_id(user_id)
        print(f"\033[35m█▓▒░ | {name} has been added to viewed_animals table \033[0m")

    return render_template('animal_details.html', context=context, animal=animal, recently_viewed_animals=recently_viewed, google_maps_api_key=GOOGLE_MAPS_KEY, google_geo_key=GOOGLE_GEOCODING_KEY)


@app.route('/bird/<org_id>/<animal_id>')
def show_bird_details(org_id, animal_id):
    """View detailed information about the bird with specific id."""
    
    context = {
        'title': "Adoptable Bird",
        'header': 'Adopt a Bird'
    }

    animal=crud.get_animal_by_id(animal_id)

    # Storing viewed animal to the database
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
            if animal.get('type') == 'Dog':
                image = "https://media.istockphoto.com/id/942318196/vector/dog-puppy-smiling-funny-animals-coloring-pages-cartoon-vector-illustration.jpg?s=612x612&w=0&k=20&c=VmV1zfZ56Kulm6nbf3wzeZfef3DwIHpT22lt4dK52nA="
            elif animal.get('type') == 'Cat':
                image = "https://i.etsystatic.com/7867651/r/il/929251/1234114682/il_1588xN.1234114682_1t12.jpg"
            elif animal.get('type') == "Rabbit":
                image = "https://i.etsystatic.com/21185388/r/il/dc90fa/2226677215/il_1588xN.2226677215_6bov.jpg"
            elif animal.get('type') == "Bird":
                image = "https://i.etsystatic.com/33889596/r/il/1e530a/3744462889/il_1588xN.3744462889_4k4v.jpg"
        viewed_animal = crud.create_viewed_animal(user_id, animal_id, name, type, breed, image, org_id)
        recently_viewed = crud.get_viewed_by_user_id(user_id)
        print(f"\033[35m█▓▒░ | {name} has been added to viewed_animals table \033[0m")

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
    for animal in animals:
        print(animal['name'])

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
                image = "https://media.istockphoto.com/id/942318196/vector/dog-puppy-smiling-funny-animals-coloring-pages-cartoon-vector-illustration.jpg?s=612x612&w=0&k=20&c=VmV1zfZ56Kulm6nbf3wzeZfef3DwIHpT22lt4dK52nA="
            elif animal.get('type') == 'Cat':
                image = "https://i.etsystatic.com/7867651/r/il/929251/1234114682/il_1588xN.1234114682_1t12.jpg"
            elif animal.get('type') == "Rabbit":
                image = "https://i.etsystatic.com/21185388/r/il/dc90fa/2226677215/il_1588xN.2226677215_6bov.jpg"
            elif animal.get('type') == "Bird":
                image = "https://i.etsystatic.com/33889596/r/il/1e530a/3744462889/il_1588xN.3744462889_4k4v.jpg"
        favorite = crud.create_favorite(user_id, animal_id, name, type, image, org_id)
        flash(f"{name} has been added to favorites list.", 'success')
        print(f"\033[36m█▓▒░ | Favorite has been added to database \033[0m")
    
    return redirect(request.referrer)


@app.route('/unfavorite/<animal_id>')
def unfavorite_animal(animal_id):
    """Remove the animal from favorites list."""

    logged_in_email = session.get("user_email")

    if logged_in_email is None:
        flash("Create or sign in to your account to add this pet to your favorites.", 'warning')
        return redirect('/')
    else:
        user_id = crud.get_user_by_email(logged_in_email).user_id
        animal = crud.get_animal_by_id(animal_id)
        animal_id = animal.get('id')
        crud.delete_favorite(user_id=user_id, animal_id=animal_id)
        flash(f"{animal.get('name')} has been removed from your favorites list.", 'success')
        print(f"\033[35m█▓▒░ | Favorite has been removed from db \033[0m")
    
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
    print(email)
    print(password)

    user = crud.get_user_by_email(email)
    if not user:
        flash("Account with this email doesn't exist. Please try again.", 'warning')
    elif user.password_hash != password:
        flash("Password you have entered is incorrect. Please try again.", 'warning')
    else:
        session["user_email"] = user.email
        flash(f"Welcome back, {user.first_name}!", 'success')

    return redirect('/')


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


@app.route('/user/update/zipcode', methods=["POST"])
def update_user_zipcode():
    """Update user zipcode."""

    zipcode = request.form.get('zipcode')
    email = session.get('user_email', None)
    if not email:
        flash("Please log in or create an account!", 'warning')

    user = crud.update_zipcode(email, zipcode)
    db.session.commit()
    flash("Zipcode has been updated.", 'success')
        
    return redirect(f'/user')


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