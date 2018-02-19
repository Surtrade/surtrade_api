from app import db


class Company(db.Model):
    """
    ***---------------------***
    Class: Company
    Type: models
    Updated: 03 Aug 2017
    Description:
        This class defines the Company table
    ***---------------------***
    """

    __tablename__ = 'company'

    # Define the columns of the Company table, starting with the primary key
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False, unique=True)
    code = db.Column(db.String(256), nullable=True)
    agents_left = db.Column(db.Integer, nullable=False, default=0)

    locations = db.relationship(
        'Location', order_by='Location.id', cascade="all, delete-orphan", back_populates="company")

    __mapper_args__ = {
        'polymorphic_identity': 'company'
    }

    def __init__(self, name, code, agents_left):
        """initialize with all values."""
        self.name = name
        self.code = code
        self.agents_left = agents_left

    def __repr__(self):
        return "<Company: {0} >".format(self.name)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Company.query.all()