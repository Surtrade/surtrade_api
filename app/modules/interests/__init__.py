from flask import Blueprint

# This instance of a Blueprint that represents the Interest blueprint
interest_blueprint = Blueprint('interest', __name__)

from app.modules.interests import views
