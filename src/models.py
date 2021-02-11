from flask_login import UserMixin

from src.configs import db

user_contacts = db.Table('user_contacts',
                         db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
                         db.Column('contact_id', db.Integer, db.ForeignKey('contacts.id'), primary_key=True)
                         )

organization_contacts = db.Table('organization_contacts',
                                 db.Column('organization_id', db.Integer, db.ForeignKey('organizations.id'),
                                           primary_key=True),
                                 db.Column('contact_id', db.Integer, db.ForeignKey('contacts.id'), primary_key=True)
                                 )


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    unique_id = db.Column(db.String(200), unique=True, nullable=False)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    picture = db.Column(db.String(200), nullable=True)
    given_name = db.Column(db.String(80))
    family_name = db.Column(db.String(80))
    locale = db.Column(db.String(10))
    contacts = db.relationship('Contact', secondary=user_contacts, lazy='subquery',
                               backref=db.backref('contact_users', lazy=True))

    def __repr__(self):
        return f'<User {self.name}, email: {self.email}>'


class Organization(db.Model):
    __tablename__ = 'organizations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    contacts = db.relationship('Contact', secondary=organization_contacts, lazy='subquery',
                               backref=db.backref('contact_organizations', lazy=True))

    def __repr__(self):
        return f'<Organization {self.name}>'


class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<Contact {self.email}>'
