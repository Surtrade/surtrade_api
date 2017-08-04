from app.common.enums import MethodsEnum, SecurityLevelEnum

from app import db


class ApiCatalog(db.Model):
    """
    ***---------------------***
    Class: ApiCatalog
    Type: models
    Updated: 03 Aug 2017
    Description:
        This class defines the API Catalog table
    ***---------------------***
    """

    __tablename__ = 'apiCatalog'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False, unique=True)
    method = db.Column(db.Enum(MethodsEnum), nullable=False)
    url = db.Column(db.String(256), nullable=False)
    description = db.Column(db.Text)
    details = db.Column(db.JSON)
    security_level = db.Column(db.Enum(SecurityLevelEnum))
    last_modified = db.Column(db.DateTime, default=db.func.current_timestamp())

    __mapper_args__ = {
        'polymorphic_identity': 'apiCatalog'
    }

    def __init__(self, name, method, url, description, details, security_level):
        self.name = name
        self.method = method
        self.url = url
        self.description = description
        self.details = details
        self.security_level = security_level

    def __repr__(self):
        return '<name:{}, method: {}>'.format(self.name, self.method)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return ApiCatalog.query.all()

    @staticmethod
    def get_one(id):
        return ApiCatalog.query.filter_by(id=id).first()
