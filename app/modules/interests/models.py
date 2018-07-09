from app import db
from datetime import datetime
from app.modules.users.models import Customer
from app.modules.locations.models import Beacon

class Interest(db.Model):
    """
    ***---------------------***
    Class: Interest
    Type: models
    Updated: 9 July 2018
    Description:
        This class defines the Interest table
    ***---------------------***
    """

    __tablename__ = 'interest'

    # Define the columns of the Interest table, starting with the primary key
    id = db.Column(db.Integer, primary_key=True)

    # Connection to customer
    # customer_id = db.Column(db.Integer, db.ForeignKey(Customer.id))
    # customer = db.relationship("Customer", back_populates="interests")
    customer_id = db.Column(db.Integer, default=True) # simple reference
    # Connection to beacon
    # beacon_id = db.Column(db.Integer, db.ForeignKey(Beacon.id))
    # beacon = db.relationship("Beacon", back_populates="interests")
    beacon = db.Column(db.String(255), default=True) # simple reference

    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    creating = db.Column(db.Boolean, default=True)
    active = db.Column(db.Boolean, default=True)
    keywords = db.Column(db.JSON)

    __mapper_args__ = {
        'polymorphic_identity': 'interest'
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
        return "<Interest of customer {0} in beacon {1}>".format(self.customer_id, self.beacon)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Interest.query.all()