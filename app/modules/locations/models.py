from app import db


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
    # lat = db.Column(db.Numeric(10, 6), nullable=False)
    # lng = db.Column(db.Numeric(10, 6), nullable=False)
    # type = db.Column(db.String(256), nullable=True)

    agents = db.relationship('Agent', order_by='Agent.id',
                             cascade="all, delete-orphan", back_populates="location")

    __mapper_args__ = {
        'polymorphic_identity': 'location',
    }

    def __init__(self, name, address, geolocation):
        """initialize with all values."""
        self.name = name
        self.address = address
        self.geolocation = geolocation
        # self.lat = lat
        # self.lng = lng
        # self.type = type

    def save(self):
        db.session.add(self)
        db.session.commit()

    def get_agents_in_location(self):
        return self.agents

    @staticmethod
    def get_all():
        return Location.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Location: {0} >".format(self.name)
