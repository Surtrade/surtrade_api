from app import db
from datetime import datetime
from app.modules.users.models import Customer
from app.modules.locations.models import Beacon

class Visit(db.Model):
    """
    ***---------------------***
    Class: Visit
    Type: models
    Updated: 27 May 2018
    Description:
        This class defines the Visit table
    ***---------------------***
    """

    __tablename__ = 'visit'

    # Define the columns of the Visit table, starting with the primary key
    id = db.Column(db.Integer, primary_key=True)

    # Connection to customer
    # customer_id = db.Column(db.Integer, db.ForeignKey(Customer.id))
    # customer = db.relationship("Customer", back_populates="visits")
    customer_id = db.Column(db.Integer, default=True) # simple reference
    # Connection to beacon
    # beacon_id = db.Column(db.Integer, db.ForeignKey(Beacon.id))
    # beacon = db.relationship("Beacon", back_populates="visits")
    beacon = db.Column(db.String(255), default=True) # simple reference

    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    creating = db.Column(db.Boolean, default=True)
    active = db.Column(db.Boolean, default=True)
    keywords = db.Column(db.JSON)

    __mapper_args__ = {
        'polymorphic_identity': 'visit'
    }

    def __init__(self, _customer_id, _beacon, _start = datetime.utcnow(), _end = datetime.utcnow()):

        """initialize with all values."""
        self.customer_id = _customer_id
        self.beacon = _beacon
        self.start = _start
        self.end = _end
        self.creating = True
        self.active = True

    def __repr__(self):
        return "<Visit of customer {0} to beacon {1}>".format(self.customer_id, self.beacon)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Visit.query.all()