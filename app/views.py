"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app, db
from flask import render_template, request, jsonify, send_file
from flask_wtf.csrf import generate_csrf
from werkzeug.utils import secure_filename
import os
import json
from .forms import MovieForm
from .models import Movie


###
# Routing for your application.
###

def get_poster(filename):
    return "http://127.0.0.1:8080/"+ os.path.join(app.config["STATIC_FOLDER"], secure_filename(filename))

@app.route('/api/v1/movies', methods=["GET"])
def get_movies():
    raw_data = db.session.query(Movie).all()
    data = list(map(lambda x: 
        {
            "id":x.id,
            "title":x.title,
            "description":x.description,
            "poster":get_poster(x.poster)
         }, raw_data))
    return jsonify(data)

@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})

@app.route('/api/v1/movies', methods=['POST'])
def save_movie():
    form = MovieForm()
    
    if form.validate_on_submit():
        [title, desc, poster, token] = form
        path = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(poster.data.filename))
        poster.data.save(path)
        
        m = Movie(title=title.data, description=desc.data, poster=secure_filename(poster.data.filename))
        
        db.session.add(m)
        db.session.commit()
        data = {
            "message": "Movie Successfully added",
            "title": m.title,
            "poster": m.poster,
            "description": m.description
        }
        return json.dumps(data)
    else:
        form_error = form_errors(form)
        data = {"errors" : form_error}
        return json.dumps(data)
    
@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404