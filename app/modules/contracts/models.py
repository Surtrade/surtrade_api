from datetime import datetime
import json

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

    __tablename__ = 'contract'

    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True)
    # Refactoring
    # agent_id = db.Column(db.Integer, db.ForeignKey('agent.id'), primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), primary_key=True)

    status = db.Column(db.Boolean, nullable=False, default=True)
    auto_authorize = db.Column(db.Boolean, default=False)
    expire = db.Column(db.DateTime)
    options = db.Column(db.JSON)

    # Objects referencing back to
    customer = db.relationship("Customer", backref=db.backref("contract", cascade="all, delete-orphan"))
    # Refactoring
    # agent = db.relationship("Agent", backref=db.backref("contract", cascade="all, delete-orphan"))
    location = db.relationship("Location", backref=db.backref("contract", cascade="all, delete-orphan"))

    __mapper_args__ = {
        'polymorphic_identity': 'contract'
    }

    # Refactoring
    def __init__(self, customer_id, location_id, auto_authorize, expire, options):
    # def __init__(self, customer_id, agent_id, auto_authorize, expire, options):
        self.customer_id = customer_id
        # self.agent_id = agent_id
        self.location_id = location_id
        self.status = True
        self.auto_authorize = auto_authorize
        self.expire = expire
        self.options = options

    def __repr__(self):
        return '<Contract between {0} and {1} >'.format(self.customer.id, self.location.id)
            # .format(self.id, self.customer.name, self.agent.name, self.expire, self.options)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def expireContract(self):
        self.status = False
        self.save()

    # This method verifies the status of a contract
    # if necessary, it expires it.
    def check_status(self):
        print("Checking status.. ")
        # if status is false then it is directly returned
        if not self.status:
            return self.status

        print(".. it was true")

        options = self.options
        # print("options expire_method 1: " + str(options.expire_method))
        print("options expire_method type: " + str(type(options)))
        print("options expire_method 2: " + str(options['expire_method']))

        # Verify Contract Options
        if options:
            print("options: " + str(options))
            if options['expire_method'] == 'time':
                print("expire "+ str(self.expire))
                if self.expire < datetime.utcnow():
                    print("expiring the contract because options expire method is time")
                    self.status = False
                    self.save()
            # elif expire_method == 'location'

        # if there are no contract options location is more important than expire time
        # if user in location then active, if not then expire
        # elif not Customer.in_location():
        #     print("expiring the contract because out of location")
        #     self.status = False
        #     self.save()

        return self.status

    def out_of_location(self):
        self.status = False
        self.save()

    @staticmethod
    def get_all():
        return Contract.query.all()

    # Refactoring
    # @staticmethod
    # def get_one(customer_id, agent_id):
    #     return Contract.query.filter_by(customer_id=customer_id, agent_id=agent_id).first()

    @staticmethod
    def get_one(customer_id, location_id):
        return Contract.query.filter_by(customer_id=customer_id, location_id=location_id).first()

