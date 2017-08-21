from app import db
from app.modules.companies.models import Company


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
