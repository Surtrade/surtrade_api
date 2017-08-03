# /app/auth/views.py

from flask import make_response, request, jsonify
from flask.views import MethodView

from . import auth_blueprint
from app.modules.users.models import User, Customer, Agent


class RegistrationView(MethodView):
    """This class registers a new user."""

    def post(self):
        """Handle POST request for this view. Url ---> /auth/register"""

        # Query to see if the user already exists
        user = User.query.filter_by(email=request.data['email']).first()

        if not user:
            # There is no user so we'll try to register them
            try:
                post_data = request.data
                # Register the user
                email = post_data['email']
                password = post_data['password']
                name = post_data['name']
                username = post_data['username']

                if 'type' in request.data:
                    usertype = post_data['type']

                    if usertype.lower() == "customer":
                        user = Customer(
                            email=email, password=password, name=name, username=username)
                    elif usertype.lower() == "agent":
                        location_id = post_data['location_id']
                        user = Agent(email=email, password=password, name=name, username=username, location_id=location_id)
                    else:
                        user = User(email=email, password=password, name=name, username=username)

                else:
                    user = User(email=email, password=password, name=name, username=username)

                user.save()

                response = {
                    'message': 'You registered successfully. Please log in.'
                }
                # return a response notifying the user that they registered successfully
                return make_response(jsonify(response)), 201
            except Exception as e:
                # An error occured, therefore return a string message containing the error
                response = {
                    'message Exception': str(e)
                }
                return make_response(jsonify(response)), 401

        else:  # There is an existing user. We don't want to register users twice
            # Return a message to the user telling them that they they already exist
            response = {
                'message': 'User already exists. Please login.'
            }

        return make_response(jsonify(response)), 202


class LoginView(MethodView):
    """This class-based view handles user login and access token generation."""

    def post(self):
        """Handle POST request for this view. Url ---> /auth/login"""
        try:
            # Get the user object using their email/username (unique to every user)
            if 'email' in request.data:
                user = User.query.filter_by(
                    email=request.data['email']).first()
            elif 'username' in request.data:
                user = User.query.filter_by(
                    username=request.data['username']).first()
            else:
                # User does not exist. Therefore, we return an error message
                response = {
                    'message': 'Invalid email/username or password, Please try again'
                }
                return make_response(jsonify(response)), 401

            # Try to authenticate the found user using their password
            if user and user.password_is_valid(request.data['password']):
                # Generate the access token. This will be used as the authorization header
                access_token = user.generate_token(user.id)
                if access_token:
                    response = {
                        'message': 'You logged in successfully.',
                        'access_token': access_token.decode()
                    }
                    return make_response(jsonify(response)), 200
            else:
                # User does not exist. Therefore, we return an error message
                response = {
                    'message': 'Invalid email/username or password, Please try again'
                }
                return make_response(jsonify(response)), 401

        except Exception as e:
            # Create a response containing an string error message
            response = {
                'message Exception': str(e)
            }
            # Return a server error using the HTTP Error Code 500 (Internal Server Error)
            return make_response(jsonify(response)), 500


registration_view = RegistrationView.as_view('register_view')
login_view = LoginView.as_view('login_view')

# Define the rule for the registration url --->  /auth/register
# Then add the rule to the blueprint
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST'])

# Define the rule for the registration url --->  /auth/login
# Then add the rule to the blueprint
auth_blueprint.add_url_rule(
    '/auth/login',
    view_func=login_view,
    methods=['POST'])
