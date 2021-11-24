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
        show_predictions_modal = False
        return render_template("user_page.html", user=user, show_predictions_modal = False, fname = session["user_fname"], user_id = session["user_id"])

    return redirect('/')

#Go to user page/dashboard
@app.route("/user_page")
def go_to_user_page():
    show_predictions_modal = False
    return render_template("user_page.html", show_predictions_modal = False, fname = session["user_fname"], user_id = session["user_id"])

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
    url1 = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

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

        response = requests.get(url1, params=payload)
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

    # get all place ids to use in api call to get phone numbers and hours of operation
    # place_ids = []
    # for result in aggregated_data["results"]:
    #     place_ids.append(result["place_id"])
    # opening_hours_list = []
    # for restroom in place_ids:
    #     url2 = "https://maps.googleapis.com/maps/api/place/details/json"

    #     payload={
    #         'place_id': restroom,
    #         'fields': 'opening_hours',
    #         'keyword': keyword,
    #         'key': f'{api_key}'
    #     }
       
    #     res = requests.get(url2, params=payload)
    #     resp_data = res.json()
    #     opening_hours_list.append(resp_data)
    
    # # print(opening_hours_list)
    # response_data = {
    #     "resp1": aggregated_data,
    #     "hours": opening_hours_list
    # }
    # return response_data
    return aggregated_data
#show review form  
@app.route("/review_form", methods=["POST"])
def show_review_form():
    """Show review form"""
    bathroom_id = request.form.get("bathroomID")
    session["bathroom_id"] = bathroom_id
    bathroom_name = request.form.get("bathroomName")
    session["bathroomName"] = bathroom_name
    show_predictions_modal = True
    
    return render_template('user_page.html', show_predictions_modal = True, bathroom_id = session["bathroom_id"], bathroom_name = session["bathroomName"], fname = session["user_fname"], user_id = session["user_id"])

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

    return render_template('user_page.html', show_predictions_modal = False, fname = session["user_fname"], user_id = session["user_id"], bathroom_name = session["bathroomName"], bathroom_id = session["bathroom_id"])


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
   
    return render_template('/chosen_restroom_reviews.html', fname = session["user_fname"], user_id = session["user_id"],bathroom_name = bathroom_name, bathroom_id = bathroom_id, reviews = reviews)

    
# Get average rating for a particular restroom
@app.route('/average_rating', methods=['GET'])
def get_avg_rating():
    """Find aerage rating for restorom"""
    bathroom_id = request.args.get("bathroom_id")
    reviews = crud.get_all_restroom_reviews(bathroom_id)
    print(reviews)
    # print(bathroom_id)
    total_clean_points = 0
    if len(reviews) > 0:
        for review in reviews:
            print(f'review cleanliness: {review.cleanliness}')
            total_clean_points += int(review.cleanliness)
        avg_rating = int(round(total_clean_points / len(reviews), 0))
        avg_rating = f'{str(avg_rating)}/5'
        print(f'{review.bathroom_name}')
        print(f'average rating: {avg_rating}')
    else:
        avg_rating = "Not yet reviewed"
    
    return avg_rating


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


if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)