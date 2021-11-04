from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db
import crud
from jinja2 import StrictUndefined 
import os
import requests

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

#TODO ask Steve how to hide key
api_key = os.environ['API_KEY']

@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')

@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user."""
    fname = request.form.get("fname")
    lname = request.form.get("lname")
    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user:
        flash("An account already exists with this email. Try again.")
    else:
        crud.create_user(fname, lname, email, password)
        flash("Account created! Please log in.")

    return redirect("/")

@app.route("/login", methods=["POST"])
def process_login():
    """Process user login."""
    email = request.form.get("email")
    password = request.form.get("password")
    
    user = crud.get_user_by_email(email)
    print(f'user {user}, email {email} password {password}')
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
    else:
        # Log in user by storing the user's first name in session
        session["user_id"] = user.user_id
        session["user_fname"] = user.fname
        flash(f"Welcome back, {user.fname}!")
        return render_template("user_page.html", user=user)

    return redirect('/')

#TODO use request library, pass lat/lng as value to key of location in payload
#TODO return place id to be able to set bathroom id in reviews table
@app.route("/user_page/restrooms")
def get_restrooms():
    """Get closest restrooms to user location from google maps api"""
    url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=-33.8670522%2C151.1957362&radius=1500&keyword=restroom&key={api_key}'

    payload={}

    response = requests.get(url, params=payload)
    data = response.json()
    location_data= data['results']
    print(location_data)

    return render_template('/restrooms.html', data=data,location_data=location_data)

    











if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)