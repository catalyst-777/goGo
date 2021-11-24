from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A user can have many reviews."""

    __tablename__ = "user_info"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    fname = db.Column(db.String(30), nullable = False)
    lname = db.Column(db.String(30), nullable = False)
    email = db.Column(db.String(100), nullable = False, unique=True)
    password = db.Column(db.String(100), nullable = False)

    #creates relationship and gives access to reviews made by specific user
    reviews = db.relationship("Review", back_populates="user")

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'
    
class Review(db.Model):
    """A review can have one user."""

    __tablename__ = "review_info"

    review_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    bathroom_name = db.Column(db.String)
    date_time = db.Column(db.Date, nullable=False)
    cleanliness = db.Column(db.Integer, nullable = False)
    accessible = db.Column(db.Boolean)
    lgbt_friendly = db.Column(db.Boolean)
    comments = db.Column(db.Text)
    bathroom_id = db.Column(db.String, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("user_info.user_id"), nullable = False)
    
    #creates relationship and gives access to user that made review
    user = db.relationship("User", back_populates="reviews")

    def __repr__(self):
        return f'<Review review_id={self.review_id} user_id={self.user_id} bathroom_id={self.bathroom_id}>'

def example_data():
    """Create some sample data."""

    # In case this is run more than once, empty out existing data
    Review.query.delete()
    User.query.delete()
    

    # Add sample users and reviews
    r1 = Review(bathroom_name='goodRR', date_time='2021-11-01', cleanliness='3', accessible=True, lgbt_friendly=False, comments="good", bathroom_id="01", user_id="1")
    r2 = Review(bathroom_name='greatRR', date_time='2021-11-02', cleanliness='5', accessible=True, lgbt_friendly=True, comments="great", bathroom_id="02", user_id="2")
    r3 = Review(bathroom_name='badRR', date_time='2021-11-03', cleanliness='1', accessible=False, lgbt_friendly=False, comments="bad", bathroom_id="03", user_id="3")

    chani = User(fname='Chani', lname="Kynes", email="chani@arrakis.com", password="sihaya")
    usul = User(fname='Paul', lname="Atreides", email="waymaker@arrakis.com", password="maud'dib")
    feyd = User(fname='Feyd-Rautha', lname="Harkonnen", email="sting@arrakis.com", password="badGuy")
    

    db.session.add_all([r1, r2, r3, chani, usul, feyd])
    db.session.commit()


def connect_to_db(flask_app, db_uri="postgresql:///reviews", echo=True):
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