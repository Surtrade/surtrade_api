from flask import make_response, request, jsonify
from flask.views import MethodView

from app.modules.visits.models import Visit
from . import visit_blueprint


class VisitsView(MethodView):

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

                visits = Visit.query.all()

                for visit in visits:
                    obj = {
                        'id': visit.id,
                        'customer_id': visit.customer_id,
                        'beacon': visit.beacon,
                        'start': visit.start,
                        'end':visit.end,
                        'creating': visit.creating,
                        'active': visit.active,
                        'keywords': visit.keywords
                    }
                    response.append(obj)

            elif method == 'POST':

                # Query to see if the visit already exists
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




                visit = Visit( customer_id, beacon, start, end)
                # visit = Visit(customer_id, beacon)
                print("now visit.start ",visit.start)
                visit.creating = creating
                visit.active = active
                visit.keywords = keywords

                visit.save()

                response = {
                    'message': 'You registered Visit customer ''{0}'' to beacon ''{1}'' successfully.'.format(visit.customer_id, visit.beacon),
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


class OneVisitView(MethodView):
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

            visit = Visit.query.filter_by(id=id).first()

            if not visit:
                return {
                    'message': "Visit does not exist.",
                    'status': 401
                }

            if method == "GET":
                response = {
                    'id': visit.id,
                    'customer_id': visit.customer_id,
                    'beacon': visit.beacon,
                    'start': visit.start,
                    'end': visit.end,
                    'creating': visit.creating,
                    'active': visit.active,
                    'keywords': visit.keywords,
                    'status': 200
                }
            elif method == "DELETE":
                visit.delete()
                response = {
                    "message": "Visit of customer ''{0}'' to beacon ''{1}'' deleted.".format(visit.customer_id, visit.beacon),
                    'status': 200
                }
            elif method == "PUT":
                visit.customer_id = str(request.data.get('customer_id', ''))
                visit.beacon = str(request.data.get('beacon', ''))
                visit.start = str(request.data.get('start', ''))
                visit.end = str(request.data.get('end', ''))
                visit.creating = str(request.data.get('creating', ''))
                visit.active = str(request.data.get('active', ''))
                visit.keywords = str(request.data.get('keywords', ''))

                visit.save()

                response = {
                    'id': visit.id,
                    'customer_id': visit.customer_id,
                    'beacon': visit.beacon,
                    'start': visit.start,
                    'end': visit.end,
                    'creating': visit.creating,
                    'active': visit.active,
                    'keywords': visit.keywords,
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


visits_view = VisitsView.as_view('visits_view')
one_visit_view = OneVisitView.as_view('one_visit_view')

# GET
# Retrieves all visits
# POST
# Saves a new visit
visit_blueprint.add_url_rule(
    '/visits',
    view_func=visits_view,
    methods=['GET', 'POST'])

# GET
# Retrieves an specific visit depending on the visit id
# PUT
# Updates an specific visit depending on the visit id
# DELETE
# Deletes an specific visit depending on the visit id
visit_blueprint.add_url_rule(
    '/visits/<int:id>',
    view_func=one_visit_view,
    methods=['GET', 'PUT', 'DELETE'])
