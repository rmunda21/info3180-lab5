# Add any model classes for Flask-SQLAlchemy here
from app import db
from sqlalchemy.sql import func


class Movie(db.Model):
    __tablename__ = 'movies'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    poster = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=func.now())
    
    def __init__(self, title, description, poster):
         self.title = title
         self.description = description
         self.poster = poster
         
    def __repr__(self):
        return '<Movie %r>' % self.id