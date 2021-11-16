from flask import (Flask, render_template, request, flash, session, jsonify, redirect)
from model import connect_to_db
import crud
from jinja2 import StrictUndefined 
import os
import requests
from datetime import datetime

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


api_key = os.environ['API_KEY']

@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')

@app.route("/users", methods=["GET","POST"])
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
        return render_template("user_page.html", user=user, fname = session["user_fname"], user_id = session["user_id"])

    return redirect('/')

#Go to user page/dashboard
@app.route("/user_page")
def go_to_user_page():

    return render_template("user_page.html", fname = session["user_fname"], user_id = session["user_id"])

# logout user
@app.route("/log_out")
def log_out():
    """Log out user by removing the stored session"""
    for key in list(session.keys()):
     session.pop(key)
    
    flash("You are now logged out!")

    return redirect("/")

#show restrooms on map
@app.route("/restrooms", methods=['GET'])
def get_restrooms():
    """Get closest restrooms to user location from google maps api"""
    url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

    userLat = request.args.get('lat')
    userLng = request.args.get('lng')

    keywords = ['food', 'gas', 'restroom']
    data_list = []
    for keyword in keywords:
        payload={
            'location': f'{userLat},{userLng}',
            'radius': '3000',
            'keyword': keyword,
            'key': f'{api_key}'
        }

        response = requests.get(url, params=payload)
        resp_data = response.json()
        # print(keyword + ":\n" + str(len(resp_data["results"])))
        data_list.append(resp_data)
        # print(len(data_list))
  
    results_list = []
    for data in data_list:
        for result in data["results"]:
            results_list.append(result)
    
    aggregated_data = data_list[0]
    # print(data_list)
    aggregated_data["results"] = results_list
    # print(len(aggregated_data["results"]))  

    return aggregated_data

#show review form  
@app.route("/review_form", methods=["POST"])
def show_review_form():
    """Show review form"""
    bathroom_id = request.form.get("bathroomID")
    session["bathroom_id"] = bathroom_id
    bathroom_name = request.form.get("bathroomName")
    session["bathroomName"] = bathroom_name
    
    return render_template('review-form.html', bathroom_id = session["bathroom_id"], bathroom_name = session["bathroomName"], fname = session["user_fname"], user_id = session["user_id"])

#Create user review
@app.route("/review-form/createReview", methods=["POST"])
def create_review():
    """Create Review"""

    date_time = request.form.get("date-picker")
    date_time = datetime.strptime(date_time, "%Y-%m-%d")
    bathroom_id = request.form.get("bathroomID")
    bathroom_id = session["bathroom_id"]
    bathroom_name = request.form.get("bathroomName")
    bathroom_name = session["bathroomName"]
    cleanliness = request.form.get("cleanliness")
    lgbt_frendly = request.form.get("lgbt_friendly")
    if lgbt_frendly == 'Yes':
        lgbt_frendly = True
    else:
        lgbt_frendly = False
    accessible = request.form.get("accessible")
    if accessible == 'Yes':
        accessible = True
    else:
        accessible = False
    comments = request.form.get("comments")
    user_id = session["user_id"]

    crud.create_review(bathroom_name, date_time, cleanliness, accessible, lgbt_frendly, comments, bathroom_id, user_id)
    flash("Your review has been added!")

    return render_template('review-form.html', fname = session["user_fname"], user_id = session["user_id"], bathroom_name = session["bathroomName"], bathroom_id = session["bathroom_id"])


#Get all of a particular user's reviews
@app.route("/all_user_reviews", methods=["GET", "POST"])
def get_all_user_reviews():
    """Show all reviews"""
    # check if bathroomName is stored in session
    # if session.get("bathroomName") is None:
    #     session["bathroomName"] = "No restroom chosen"
    user_id = session["user_id"]
    reviews = crud.get_all_user_reviews(user_id)
   
    return render_template('/all_user_reviews.html', fname = session["user_fname"], user_id = session["user_id"], reviews = reviews)

@app.route('/all_restroom_reviews', methods=['GET', 'POST'])
def get_all_restroom_reviews():
    """Show all reviews for one restroom"""
    
    bathroom_id = request.form.get("bathroomID")
    bathroom_name = request.form.get("bathroomName")
  
    reviews = crud.get_all_restroom_reviews(bathroom_id)
    
    if len(reviews) <= 0:
        flash('This restroom has not been reviewed. Be the first to leave a review!')
        # return render_template('/chosen_restroom_reviews.html', fname = session["user_fname"], user_id = session["user_id"], bathroom_name = bathroom_name, bathroom_id = session["bathroom_id"])
   
    return render_template('/chosen_restroom_reviews.html', fname = session["user_fname"], user_id = session["user_id"],bathroom_name = bathroom_name, bathroom_id = bathroom_id, reviews = reviews)

#DELETE a user's review
@app.route('/delete_review', methods=['POST'])
def delete_review():
    """Delete review"""
    review_id = request.form.get("review_id")
    user_id = session["user_id"]
    review = crud.delete_review(review_id)
    reviews = crud.get_all_user_reviews(user_id)

    flash('Review was deleted')
    return render_template('/all_user_reviews.html', fname = session["user_fname"], user_id = session["user_id"], reviews = reviews)

# @app.route('/update_review', methods=['POST'])
# def update_review():
#     """Update review"""
#     review_id = request.form.get("review_id")
#     user_id = session["user_id"]
#     crud.delete_review(review_id)
#     reviews = crud.get_all_user_reviews(user_id)

if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)