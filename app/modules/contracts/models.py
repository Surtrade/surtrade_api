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

    __tablename__ = 'contract'

    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id'), primary_key=True)

    status = db.Column(db.Boolean, nullable=False, default=True)
    auto_authorize = db.Column(db.Boolean, default=False)
    expire = db.Column(db.DateTime)
    options = db.Column(db.JSON)

    # Objects referencing back to
    customer = db.relationship("Customer", backref=db.backref("contract", cascade="all, delete-orphan"))
    agent = db.relationship("Agent", backref=db.backref("contract", cascade="all, delete-orphan"))

    __mapper_args__ = {
        'polymorphic_identity': 'contract'
    }

    def __init__(self, customer_id, agent_id, auto_authorize, expire, options):
        self.customer_id = customer_id
        self.agent_id = agent_id
        self.status = True
        self.auto_authorize = auto_authorize
        self.expire = expire
        self.options = options

    def __repr__(self):
        return '<contract {0} between {1} and {2}. Expires: {3}>'\
            .format(self.id, self.customer.name, self.agent.name, self.expire, self.options)

    def save(self):
        db.session.add(self)
        db.session.commit()

    # This method verifies the status of a contract
    # if necessary, it expires it.
    def check_status(self):
        # if status is false then it is directly returned
        if not self.status:
            return self.status

        # Verify Contract Options
        if 'expire_method' in self.options:
            expire_method = self.options['expire_method']
            if expire_method == 'time' and not self.auto_authorize and self.expire < datetime.utcnow():
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

    @staticmethod
    def get_one(customer_id, agent_id):
        return Contract.query.filter_by(customer_id=customer_id, agent_id=agent_id).first()
