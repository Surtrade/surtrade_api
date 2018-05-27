from datetime import datetime, timedelta

import jwt
from flask import current_app
from flask_bcrypt import Bcrypt

from app import db
from app.modules.locations.models import Location
from app.modules.companies.models import Company
# from app.modules.visits.models import Visit
# from app.modules.interests.models import Interest


# Parent User Class to be extended to Customer and Agent

class User(db.Model):
    """
    ***---------------------***
    Class: User
    Type: models
    Updated: 01 Aug 2017
    Description:
        This class defines the users table for SQLAlchemy
    ***---------------------***
    """

    __tablename__ = 'user'

    # Define the columns of the users table, starting with the primary key
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(255), nullable=False)
    created_date = db.Column(db.DateTime, default=db.func.current_timestamp())

    # ALTER TABLE user ALTER COLUMN password TYPE varying(255)

    # Relationship with child classes
    type = db.Column(db.String(255), nullable=True)

    # bucketlists = db.relationship('Bucketlist', order_by='Bucketlist.id', cascade="all, delete-orphan")

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }

    def __init__(self, username, name, email, password, role):
        """Initialize the user with an email and a password."""
        self.username = username
        self.name = name
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()
        self.role = role

    def password_is_valid(self, password):
        """
        Checks the password against it's hash to validates the user's password
        """
        return Bcrypt().check_password_hash(self.password, password)

    def save(self):
        """Save a user to the database.
        This includes creating a new user and editing one.
        """
        db.session.add(self)
        db.session.commit()

    def generate_token(self, user_id):
        """ Generates the access token"""
        try:
            # set up a payload with an expiration time
            payload = {
                'exp': datetime.utcnow() + timedelta(hours=24),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            # create the byte string token using the payload and the SECRET key
            jwt_string = jwt.encode(
                payload,
                current_app.config.get('SECRET'),
                algorithm='HS256'
            )
            return jwt_string

        except Exception as e:
            # return an error in string format if an exception occurs
            return str(e)

    @staticmethod
    def decode_token(token):
        """Decodes the access token from the Authorization header."""
        try:
            # try to decode the token using our SECRET variable
            payload = jwt.decode(token, current_app.config.get('SECRET'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            # the token is expired, return an error string
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            # the token is invalid, return an error string
            return "Invalid token. Please register or login"


# Customer user extension of User Class
class Customer(User):
    """
    ***---------------------***
    Class: Customer
    Type: models
    Updated: 01 Aug 2017
    Description:
        This class defines the user Customer table for SQLAlchemy
    ***---------------------***
    """
    __tablename__ = 'customer'

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    # Many to many contract
    # Refactoring
    # agent = db.relationship("Agent", secondary="contract")
    location = db.relationship("Location", secondary="contract")

    # Reference back to Visit and Interest
    # visits = db.relationship('Visit', order_by='Visit.id', cascade="all, delete-orphan", back_populates="customer")
    # interests = db.relationship('Interests', order_by='Interest.id', cascade="all, delete-orphan", back_populates="customer")

    __mapper_args__ = {
        'polymorphic_identity': 'customer'
    }

    def __init__(self, username, email, password, name, role):
        """Initialize the user with an email and a password."""
        self.username = username
        self.name = name
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()
        self.role = role


# Agent user extension of User Class
class Agent(User):
    """
    ***---------------------***
    Class: Agent
    Type: models
    Updated: 01 Aug 2017
    Description:
        This class defines the user Agent table for SQLAlchemy
    ***---------------------***
    """
    __tablename__ = 'agent'

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    # Connection to location
    location_id = db.Column(db.Integer, db.ForeignKey(Location.id))
    location = db.relationship("Location", back_populates="agents")

    # Many to many contract
    # Refactoring
    # customers = db.relationship("Customer", secondary="contract")

    __mapper_args__ = {
        'polymorphic_identity': 'agent'
    }

    def __init__(self, username, email, password, name, location_id, role):
        """Initialize the user with an email and a password."""
        self.username = username
        self.name = name
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()
        self.location_id = location_id
        self.role = role
