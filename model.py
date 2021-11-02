from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = "user_info"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    fname = db.Column(db.String(30), nullable = False)
    lname = db.Column(db.String(30), nullable = False)
    email = db.Column(db.String(100), nullable = False, unique=True)
    password = db.Column(db.String(100), nullable = False)

    #creates relationship and gives access to reviews made by specific user
    reviews = db.relationship("Reviews", back_populates="user")

    def __repr__(self):
        return f'<User user_id={self.user_id}email={self.email}>'
    
class Reviews(db.Model):
    """A user can have multiple reviews."""

    __tablename__ = "review_info"

    review_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    date_time = db.column(db.DateTime)
    cleanliness = db.Column(db.Integer, nullable = False)
    accessibile = db.Column(db.Boolean)
    lgbt_friendly = db.Column(db.Boolean)
    comments = db.column(db.Text)
    #TODO find out data type of id pulled from maps api for each bathroom
    bathroom_id = db.Column(db.String, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("user_info.user_id"), nullable = False)
    
    #creates relationship and gives access to user that made review
    user = db.relationship("User", back_populates="reviews")

    def __repr__(self):
        return f'<Reviews review_id={self.review_id} cleanliness={self.cleanliness}>'


#TODO be sure to call db "reviews"
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