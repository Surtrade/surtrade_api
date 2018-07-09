from flask import make_response, request, jsonify
from flask.views import MethodView

from app.modules.interests.models import Interest
from app.modules.interests import interest_blueprint


class InterestsView(MethodView):

    def action(self, method):

        from app.modules.users.models import User

        try:
            # Get the access token from the header
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return {
                    'message': "Token missing.",
                    'status': 400
                }
            access_token = auth_header.split(" ")[1]

            if not access_token or isinstance(User.decode_token(access_token), str):
                # Attempt to decode the token and get the User ID
                return {
                    'message': "Authentication token error.",
                    'status': 511
                }

            response = []

            if method == "GET":

                interests = Interest.query.all()

                for interest in interests:
                    obj = {
                        'id': interest.id,
                        'customer_id': interest.customer_id,
                        'beacon': interest.beacon,
                        'start': interest.start,
                        'end':interest.end,
                        'creating': interest.creating,
                        'active': interest.active,
                        'keywords': interest.keywords
                    }
                    response.append(obj)

            elif method == 'POST':

                # Query to see if the interest already exists
                post_data = request.data

                customer_id = post_data['customer_id']
                beacon = post_data['beacon']
                start = post_data['start']
                end = post_data['end']
                creating = post_data['creating']
                active = post_data['active']
                keywords = post_data['keywords']
                print ("customer_id ",customer_id)
                print ("beacon ", beacon)
                print("now ",)
                print ("start ", start)
                print ("end ", end)
                print ("creating ", creating)
                print ("active ",active)
                print ("keywords ", keywords)

                interest = Interest( customer_id, beacon, start, end)
                # interest = Interest(customer_id, beacon)
                print("now interest.start ",interest.start)
                interest.creating = creating
                interest.active = active
                interest.keywords = keywords

                interest.save()

                response = {
                    'message': 'You registered Interest of customer ''{0}'' to beacon ''{1}'' successfully.'.format(interest.customer_id, interest.beacon),
                    'status': 201
                }

            return response

        except Exception as e:
            # Create a response containing an string error message
            return {
                'message': str(e),
                'status': 500
            }

    def get(self):
        response = self.action('GET')
        if 'status' in response:
            status = response['status']
            del response['status']
        else:
            status = 200

        return make_response(jsonify(response)), status

    def post(self):
        response = self.action('POST')
        if 'status' in response:
            status = response['status']
            del response['status']
        else:
            status = 200

        return make_response(jsonify(response)), status


class OneInterestView(MethodView):
    def action(self, method, id):
        from app.modules.users.models import User

        try:
            # Get the access token from the header
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return {
                    'message': "Token missing.",
                    'status': 400
                }

            access_token = auth_header.split(" ")[1]

            # Verify correct token
            if not access_token or isinstance(User.decode_token(access_token), str):
                # Attempt to decode the token and get the User ID
                return {
                    'message': "Authentication token error.",
                    'status': 511
                }

            response = {}

            interest = Interest.query.filter_by(id=id).first()

            if not interest:
                return {
                    'message': "Interest does not exist.",
                    'status': 401
                }

            if method == "GET":
                response = {
                    'id': interest.id,
                    'customer_id': interest.customer_id,
                    'beacon': interest.beacon,
                    'start': interest.start,
                    'end': interest.end,
                    'creating': interest.creating,
                    'active': interest.active,
                    'keywords': interest.keywords,
                    'status': 200
                }
            elif method == "DELETE":
                interest.delete()
                response = {
                    "message": "Interest of customer ''{0}'' to beacon ''{1}'' deleted.".format(interest.customer_id, interest.beacon),
                    'status': 200
                }
            elif method == "PUT":
                interest.customer_id = str(request.data.get('customer_id', ''))
                interest.beacon = str(request.data.get('beacon', ''))
                interest.start = str(request.data.get('start', ''))
                interest.end = str(request.data.get('end', ''))
                interest.creating = str(request.data.get('creating', ''))
                interest.active = str(request.data.get('active', ''))
                interest.keywords = str(request.data.get('keywords', ''))

                interest.save()

                response = {
                    'id': interest.id,
                    'customer_id': interest.customer_id,
                    'beacon': interest.beacon,
                    'start': interest.start,
                    'end': interest.end,
                    'creating': interest.creating,
                    'active':  interest.active,
                    'keywords': interest.keywords,
                    'status': 200
                }

            return response

        except Exception as e:
            # Create a response containing a string error message
            response = {
                'message': str(e),
                'status': 500
            }

            return response
            # return make_response(jsonify(response)), 500

    def get(self, id):
        response = self.action('GET', id)
        status = response['status']
        del response['status']

        return make_response(jsonify(response)), status

    def delete(self, id):
        response = self.action('DELETE', id)
        status = response['status']
        del response['status']

        return make_response(jsonify(response)), status

    def put(self, id):
        # return make_response(jsonify({'message': 'Test'})), 200
        response = self.action('PUT', id)
        status = response['status']
        del response['status']

        return make_response(jsonify(response)), status


interests_view = InterestsView.as_view('interests_view')
one_interest_view = OneInterestView.as_view('one_interest_view')

# GET
# Retrieves all interests
# POST
# Saves a new interest
interest_blueprint.add_url_rule(
    '/interests',
    view_func=interests_view,
    methods=['GET', 'POST'])

# GET
# Retrieves an specific interest depending on the interest id
# PUT
# Updates an specific interest depending on the interest id
# DELETE
# Deletes an specific interest depending on the interest id
interest_blueprint.add_url_rule(
    '/interests/<int:id>',
    view_func=one_interest_view,
    methods=['GET', 'PUT', 'DELETE'])
