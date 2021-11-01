from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = "user_info"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    fname = db.Column(db.String)
    lname = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    def __repr__(self):
        return f'<User user_id={self.user_id}email={self.email}>'
    
class Reviews(db.Model):
    """A user can have multiple reviews."""

    __tablename__ = "review_info"

    review_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    cleanliness = db.Column(db.Integer)
    accessibile = db.Column(db.Boolean)
    lgbt_friendly = db.Column(db.Boolean)
    comments = db.column(db.Text)
    #TODO find out data type of id pulled from maps api for each bathroom
    bathroom_id = db.Column(db.String, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("user_info.user_id"))
    
    user = db.relationship("User", backref="ratings_info") #attribute added, returns a list of Ratings

    def __repr__(self):
        return f'<Reviews review_id={self.review_id} cleanliness={self.cleanliness}>'

def connect_to_db(flask_app, db_uri="postgresql:///reviews", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__": #does something so we can use our application
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)