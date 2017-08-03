from datetime import datetime

from app import db


class Contract(db.Model):
    """
    ***---------------------***
    Class: Contract
    Type: models
    Updated: 01 Aug 2017
    Description:
        This class defines the Contract table for SQLAlchemy
        Many to many Class
    ***---------------------***
    """

    __tablename__ = 'contracts'

    customer_id = db.Column(db.Integer, db.ForeignKey(
        'customer.id'), primary_key=True)
    agent_id = db.Column(db.Integer, db.ForeignKey(
        'agent.id'), primary_key=True)

    status = db.Column(db.Boolean, default=True)
    auto_authorize = db.Column(db.Boolean, default=False)
    expire = db.Column(db.DateTime)

    # Objects referencing back to
    customer = db.relationship("Customer", backref=db.backref(
        "contracts", cascade="all, delete-orphan"))
    agent = db.relationship("Agent", backref=db.backref(
        "contracts", cascade="all, delete-orphan"))

    __mapper_args__ = {
        'polymorphic_identity': 'contracts'
    }

    def __init__(self, customer_id, agent_id, auto_authorize, expire):
        self.customer_id = customer_id
        self.agent_id = agent_id
        self.status = True
        self.auto_authorize = auto_authorize
        self.expire = expire

    def __repr__(self):
        return '<contracts {0} between {1} and {2}. Expires: {3}>'.format(self.id, self.customer.name,
                                                                                   self.agent.name, self.expire)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def check_expire(self):
        if self.expire < datetime.utcnow() and not self.auto_authorize and self.status == True:
            print("expiring the contracts")
            self.status = False
            self.save()

        return self.status

    @staticmethod
    def get_all():
        return Contract.query.all()

    @staticmethod
    def get_one(customer_id, agent_id):
        return Contract.query.filter_by(customer_id=customer_id, agent_id=agent_id).first()
