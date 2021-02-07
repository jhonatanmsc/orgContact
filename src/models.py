from flask_login import UserMixin

from src.configs import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    unique_id = db.Column(db.String(200), unique=True, nullable=False)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    picture = db.Column(db.String(200), nullable=True)
    given_name = db.Column(db.String(80))
    family_name = db.Column(db.String(80))
    locale = db.Column(db.String(10))

    def __init__(self, unique_id, name, email, picture, given_name, family_name, locale):
        self.unique_id = unique_id
        self.name = name
        self.email = email
        self.picture = picture
        self.given_name = given_name
        self.family_name = family_name
        self.locale = locale

    def __repr__(self):
        return f'<User {self.name}, email: {self.email}>'
