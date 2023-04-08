# Add any form classes for Flask-WTF here
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.fields import StringField, TextAreaField
from wtforms.validators import InputRequired

class Movie():
    title = StringField(validators=[InputRequired()])
    desc = TextAreaField(validators=[InputRequired()])
    poster = FileField(validators=[FileRequired(), FileAllowed(['png', 'jpeg', 'jpg'], "png, jpeg and jpg allowed")])