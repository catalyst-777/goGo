"""CRUD operations."""
from model import db, User, Review, connect_to_db

# CRUD for users
def create_user(fname, lname, email, password):
    """Create and return a new user."""

    user = User(fname=fname, lname=lname, email=email, password=password)

    db.session.add(user)
    db.session.commit()

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

# CRUD for reviews
def create_review(bathroom_name, date_time, cleanliness, accessible, lgbt_friendly, comments, bathroom_id, user_id):
    """Create and return a new review"""
    review = Review(bathroom_name=bathroom_name, date_time=date_time, cleanliness=cleanliness, accessible=accessible, lgbt_friendly=lgbt_friendly, comments=comments, bathroom_id=bathroom_id, user_id=user_id)

    db.session.add(review)
    db.session.commit()

    return review

def get_all_user_reviews(user_id):
    """Return all reviews from one user"""
    user = User.query.filter(User.user_id == user_id).first()

    return user.reviews

def get_all_restroom_reviews(bathroom_id):
    """Retrun all reviews for one restroom"""
    
    reviews = Review.query.filter(Review.bathroom_id == bathroom_id).all()
    
    return reviews

def delete_review(review_id):
    print(review_id)
    review = Review.query.filter(Review.review_id == review_id).first()
    print(review)
    db.session.delete(review)
    db.session.commit()


def update_review(review_id):
    print(review_id)
    



if __name__ == "__main__":
    from server import app

    connect_to_db(app)