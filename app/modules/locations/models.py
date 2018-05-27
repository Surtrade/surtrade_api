from app import db
from app.modules.companies.models import Company
# from app.modules.visits.models import Visit
# from app.modules.interests.models import Interest
from app.common.enums import BeaconRoleEnum


class Location(db.Model):
    """
    ***---------------------***
    Class: Location
    Type: models
    Updated: 01 Aug 2017
    Description:
        This class defines the location table
    ***---------------------***
    """

    __tablename__ = 'location'

    # Define the columns of the location table, starting with the primary key
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False, unique=True)
    address = db.Column(db.String(256), nullable=True)
    geolocation = db.Column(db.JSON)

    # Connection to company
    company_id = db.Column(db.Integer, db.ForeignKey(Company.id))
    company = db.relationship("Company", back_populates="locations")

    agents = db.relationship('Agent', order_by='Agent.id',
                             cascade="all, delete-orphan", back_populates="location")

    beacons = db.relationship(
        'Beacon', order_by='Beacon.id', cascade="all, delete-orphan", back_populates="location")

    # Many to many contract
    # Refactoring
    customers = db.relationship("Customer", secondary="contract")

    __mapper_args__ = {
        'polymorphic_identity': 'location',
    }

    def __init__(self, name, address, geolocation, company_id):
        """initialize with all values."""
        self.name = name
        self.address = address
        self.geolocation = geolocation
        self.company_id = company_id

    def __repr__(self):
        return "<Location: {0} >".format(self.name)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def get_agents_in_location(self):
        return self.agents

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Location.query.all()

# Beacon class - Beacons inside a Location
class Beacon(db.Model):
    """
    ***---------------------***
    Class: Beacon
    Type: models
    Updated: 07 Feb 2018
    Description:
        This class defines the Beacon table for SQLAlchemy
    ***---------------------***
    """
    __tablename__ = 'beacon'

    id = db.Column(db.Integer, primary_key=True)
    # role = db.Column(db.Enum(BeaconRoleEnum), nullable=False)
    role = db.Column(db.String(255), nullable=False)
    identificator = db.Column(db.String(255), nullable=False, unique=True)
    major = db.Column(db.String(255), nullable=False)
    minor = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=True)
    active = db.Column(db.Boolean, default=True)
    keywords = db.Column(db.JSON)

    # Connection to location
    location_id = db.Column(db.Integer, db.ForeignKey(Location.id))
    location = db.relationship("Location", back_populates="beacons")


    # Reference back to Visit and Interest
    # visits = db.relationship('Visit', order_by='Visit.id', cascade="all, delete-orphan", back_populates="customer")
    # interests = db.relationship('Interests', order_by='Interest.id', cascade="all, delete-orphan", back_populates="customer")

    __mapper_args__ = {
        'polymorphic_identity': 'beacon'
    }

    def __init__(self, major, minor, location_id, role="store", name="beacon"):
        """Initialize the Beacon with Type and location."""
        self.major = major
        self.minor = minor
        self.identificator = str(major)+str(minor)
        # self.active = True # default: True
        self.location_id = location_id
        self.role = role
        self.name = name

    def __repr__(self):
        return "<Beacon: {0} >".format(self.identificator)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()