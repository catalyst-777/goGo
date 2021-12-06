![Logo](/static/img/gogo_logo_purpleBackground.png)
goGo

Anyone who has traveled or been in an unfamiliar area knows the feeling; you're out and about and suddenly you gotta goGO, you know? We want to know where we can goGo and how to get there, but we have other questions too. Will the restroom be clean, safe, LGBTQ+ friendly, and handicap accessible? goGO answers all those questions through a clean and easy-to-navigate interface. goGo users can: find their location,  find restrooms within a 2-mile radius, get the route to the restroom of their choice, leave reviews based on cleanliness, lgbtq+ friendliness, and handicap-accessibility, view their previous reviews and delete them if desired, and see reviews of the restroom of their choice.

## Table of Contents

* [Tech Stack](#tech-stack)
* [Features](#features)
* [Setup/Installation](#installation)
* [To-Do](#future)

## <a name="tech-stack"></a>Tech Stack

__Frontend:__ Javascript, jQuery, jinja2, Bootstrap, CSS, HTML <br/>
__Backend:__ Python, Flask, SQLAlchemy, PostgreSQL <br/>
__APIs:__ Google Maps Platform: maps, routes, places <br/>

## <a name="features"></a>Features

Login to get goGo-ing! 
![Login](/static/img/login.gif)
<br/><br/><br/>


Get directions to restroom of your choice.
![Get Directions](/static/img/getDirections_gif.gif)
<br/><br/><br/>


Add your review to aid other goGO-ers in their search for the perfect restroom. 
![Add Review](/static/img/leaveReview_gif.gif)
<br/><br/><br/>
 

 View reviews of restroom of your choice.
![Restroom Reviews](/static/img/restroomReviews_gif.gif)


## <a name="installation"></a>Setup/Installation ⌨️

#### Requirements:

- PostgreSQL
- Python 3
- GoogleMaps Platform API key

To have this app running on your local computer, please follow the below steps:

Clone repository:
```
$ git clone https://github.com/catalyst-777/goGo
```
Create a virtual environment:
```
$ virtualenv env
```
Activate the virtual environment:
```
$ source env/bin/activate
```
Install dependencies:
```
$ pip install -r requirements.txt
```
Get your own secret key🔑 for [Google Maps Platform](https://support.google.com/googleapi/answer/6158862?hl=en). Save them to a file `secrets.py`. Your file should look something like this:
```
API_KEY = 'abc'
```
Create database 'reviews'.
```
$ createdb reviews
```
Create your database tables and seed example data.
```
$ python3 model.py
$ psql reviews < goGO-reviews.sql
```
Run the app from the command line.
```
$ python3 server.py
```
If you want to use SQLAlchemy to query the database, run in interactive mode
```
$ python3 -i model.py
```

## <a name="future"></a>TODO✨
* The ability for user to add image  of restroom to their review
* Provide more personalized user profile
* Add google O-auth
