from app import db
from datetime import datetime
import json

shelf_product = db.Table('shelf_product',
                    db.Column('product_id', db.ForeignKey('product.id'), primary_key=True),
                    db.Column('shelf_id', db.ForeignKey('shelf.id'), primary_key=True),
            )


class Shelf(db.Model):
    """
    ***---------------------***
    Class: Shelf
    Type: models
    Updated: 17 Jul 2017
    Description:
        This class defines the shelf table
    ***---------------------***
    """

    __tablename__ = 'shelf'

    # Define the columns of the Shelf table, starting with the primary key
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(256), nullable=False)
    beacon = db.Column(db.String(256), nullable=False)
    created_dt = db.Column(db.DateTime)
    keywords = db.Column(db.JSON)
    active = db.Column(db.Boolean, default=True)

    # Connection to products
    # products = db.relationship("Product",
    #                 secondary=shelf_product,
    #                 backref="shelves")
    products = db.relationship("Product",
                               secondary=shelf_product)
    # products = db.relationship('Product', secondary=products, lazy='subquery',
    #                        backref=db.backref('shelves', lazy=True))
    # products = db.relationship('Product', backref='shelf', lazy=True)
    # products = db.relationship('Product', order_by='Product.id', cascade="all, delete-orphan", back_populates="shelf")
    # product_id = db.Column(db.Integer, db.ForeignKey(Product.id))
    # product = db.relationship("Product", back_populates="shelves")
    # products = relationship("Product", back_populates="shelf")
    # products = relationship("Product", backref="shelf")

    __mapper_args__ = {
        'polymorphic_identity': 'shelf',
    }

    def __init__(self, code, beacon):
        """initialize with all values."""
        self.code = code
        self.beacon = beacon
        self.created_dt = datetime.utcnow()


    def __repr__(self):
        return "<Shelf: {0} >".format(self.code)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Shelf.query.all()

# Product class - Products in a shelf
class Product(db.Model):
    """
    ***---------------------***
    Class: Product
    Type: models
    Updated: 17 Jul 2018
    Description:
        This class defines the Product table for SQLAlchemy
    ***---------------------***
    """
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(255), nullable=False)#, unique=True)
    name = db.Column(db.String(255), nullable=True)
    description = db.Column(db.String(255), nullable=True)
    created_dt = db.Column(db.DateTime)
    keywords = db.Column(db.JSON)
    image = db.Column(db.String(255), nullable=True)
    video = db.Column(db.String(255), nullable=True)
    remark = db.Column(db.String(255), nullable=True)

    # Connection to shelf
    # shelf_id = db.Column(db.Integer, db.ForeignKey('shelf.id'), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'product'
    }

    def __init__(self, code, name, description=""):
        """Initialize the Product."""
        self.code = code
        self.name = name
        self.description = description
        self.created_dt = datetime.utcnow()
        self.shelf = []

    def __repr__(self):
        # return "<Product: {0} >".format(self.name)
        # return json.dumps(self.__dict__)
        return json.dumps({"code":self.code,"name":self.name,"description":self.description, "keywords":self.keywords, "image":self.image, "video":self.video, "remark":self.remark})
        # return json.load({"name":self.name,"description":self.description})
        # return jsonify({"name":self.name,"description":self.description})
        # return {"name":self.name,"description":self.description}


    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()