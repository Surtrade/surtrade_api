from flask import Blueprint

# This instance of a Blueprint that represents the Contract blueprint
apiCatalog_blueprint = Blueprint('apiCatalog', __name__)

from . import views
