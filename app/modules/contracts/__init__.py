from flask import Blueprint

# This instance of a Blueprint that represents the Contract blueprint
contract_blueprint = Blueprint('Contract', __name__)

from . import views
