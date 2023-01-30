# HappyPaws


## Summary

**HappyPaws** is a a pet adoption website dedicated to finding loving homes for homeless animals in need. HappyPaws connects pet owners with the perfect pet for their family.


## About the Developer

HappyPaws was created by Assema Nurakhmetova. Learn more about the developer on [LinkedIn](https://www.linkedin.com/in/assemanur/).


## Technologies

**Tech Stack:**

- Python
- Flask
- SQLAlchemy
- PostgreSQL
- Jinja2
- HTML
- CSS
- Javascript
- JSON
- Bootstrap
- Petfinder API
- Google Maps API
- Google Geocoding API
- IP-API

HappyPaws is an app built on a Flask server with a PostgreSQL database, with SQLAlchemy as the ORM. The front end templating uses Jinja2, the HTML was built using Bootstrap, and Javascript to interact with the backend. Animals view is rendered with Petfinder API. The map is built using the Google Maps API, zipcodes are converted into geographic coordinates with Google Geocoding API.

## <a name="features"></a>Features

Users can browse animals by animal type (dog, cat, rabbit, or bird):
![](https://github.com/assemanur/happypaws/blob/main/static/img/readme/categories.png "Search animals by category")

Users can also browse organizations nearby:
![](https://github.com/assemanur/happypaws/blob/main/static/img/readme/search_organizations.png "Search organizations")

User can also search animals by the breed and zipcode: 
![](https://github.com/assemanur/happypaws/blob/main/static/img/readme/custom_search.png "Search by the breed and zipcode")

Users can view animal details and approximate location of the animal on the map:
![](https://github.com/assemanur/happypaws/blob/main/static/img/readme/animal_details_1.png "View animal details")

Users can create or sign in to existing account:
![](https://github.com/assemanur/happypaws/blob/main/static/img/readme/sign_in.png "Sign in to HappyPaws")

Users can favorite animals:
![](https://github.com/assemanur/happypaws/blob/main/static/img/readme/favorite.png "Favorite button")

Users can see favorited animals:
![](https://github.com/assemanur/happypaws/blob/main/static/img/readme/favorites.png "Viewing favorited animals")

Users can also update their profile information:
![](https://github.com/assemanur/happypaws/blob/main/static/img/readme/user_profile.png "Updating user profile details")

If interested in adopting, users can send email inquiry to the organization:
![](https://github.com/assemanur/happypaws/blob/main/static/img/readme/email%20inquiry.png "Send email inquiry")

## <a name="installation"></a>Setup/Installation ⌨️

#### Requirements:

- PostgreSQL
- Python 3.10
- Petfinder, Google Maps and Google Geocoding API keys

To have this app running on your local computer, please follow the below steps:

Clone repository:
```
$ git clone https://github.com/assemanur/happypaws.git
```
Create a virtual environment🔮:
```
$ virtualenv env
```
Activate the virtual environment:
```
$ source env/bin/activate
```
Install dependencies🔗:
```
$ pip install -r requirements.txt
```
Get your own secret keys🔑 for [Petfinder](https://www.petfinder.com/developers/), [Google Maps](https://developers.google.com/maps/documentation/javascript/get-api-key), and [Google Geocoding](https://developers.google.com/maps/documentation/geocoding/get-api-key). Save them to a file `secrets.sh`. Your file should look something like this:
```
export PETFINDER_KEY="abc"
export PETFINDER_SECRET="abc"
export GOOGLE_MAPS_KEY="abc"
export GOOGLE_GEOCODING_KEY="abc"
```
Activate API keys.
```
$ source secrets.sh
```
Create your database and seed🌱 example data.
```
$ python3 seed_database.py
```
Run the app from the command line.
```
$ python3 server.py
```
If you want to check the database, run in interactive mode
```
$ psql pet_shelter