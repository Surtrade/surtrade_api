from flask import Blueprint

# This instance of a Blueprint that represents the Shelf blueprint
shelf_blueprint = Blueprint('shelf', __name__)
product_blueprint = Blueprint('product', __name__)

from . import views
