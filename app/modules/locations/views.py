# /app/auth/views.py
import googlemaps
from flask import make_response, request, jsonify
from flask.views import MethodView

import instance.config as config
from app.modules.locations.models import Location, Beacon
from . import location_blueprint

google_api_key = config.Config.GOOGLE_API_KEY

gmaps = googlemaps.Client(key=google_api_key)


class LocationsView(MethodView):

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

                # Return only the list of location matching the coordinates on the UR
                lat = request.args.get('lat')
                lng = request.args.get('lng')

                locations = Location.query.all()

                for location in locations:
                    if location.address == 'mobile':
                        continue

                    # If has coordinates arguments
                    if lat and lng:
                        lat = float(lat)
                        lng = float(lng)
                        latne = float(location.geolocation['bounds']['northeast']['lat'])
                        lngne = float(location.geolocation['bounds']['northeast']['lng'])
                        latsw = float(location.geolocation['bounds']['southwest']['lat'])
                        lngsw = float(location.geolocation['bounds']['southwest']['lng'])

                        # If given coordinates are in bounds of the location in loop
                        if (latne >= lat and lngne >= lng) and (latsw <= lat and lngsw <= lng):
                            obj = {
                                'id': location.id,
                                'name': location.name,
                                'address': location.address,
                                'geolocation': location.geolocation,
                                'beacons': location.beacons
                            }
                            response.append(obj)
                    else:
                        obj = {
                            'id': location.id,
                            'name': location.name,
                            'address': location.address,
                            'geolocation': location.geolocation,
                            'beacons': location.beacons
                        }
                        response.append(obj)

            elif method == 'POST':
                print("Test")
                # Query to see if the user already exists
                post_data = request.data
                # Register the location
                name = post_data['name']
                address = post_data['address']

                location = Location.query.filter_by(name=name).first()
                company_id = post_data['company_id']
                # beacons = post_data['beacons']

                if location:
                    return {
                        'message': 'Location already exists. Please use a different name.',
                        'status': 202
                    }

                if address.lower() == 'mobile':
                    geolocation = {
                        'location_type': 'mobile'
                    }

                else:
                    address = post_data['address']

                    # Geocoding an address
                    geocode_result = gmaps.geocode(address)
                    address = geocode_result[0]['formatted_address']
                    geolocation = geocode_result[0]['geometry']

                    if 'bounds' not in geolocation:
                        # add fictional bounds
                        geolocation.update({
                            'bounds': {
                                'northeast': {
                                    'lat': geolocation['location']['lat'] + 0.0002,
                                    'lng': geolocation['location']['lng'] + 0.0002
                                },
                                'southwest': {
                                    'lat': geolocation['location']['lat'] - 0.0002,
                                    'lng': geolocation['location']['lng'] - 0.0002
                                }
                            }
                        })

                location = Location(
                    name=name, address=address, geolocation=geolocation, company_id=company_id)

                location.save()

                response = {
                    'message': 'You registered location ''{0}'' successfully.'.format(location.name),
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


class OneLocationVew(MethodView):
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

            location = Location.query.filter_by(id=id).first()

            if not location:
                return {
                    'message': "Location does not exist.",
                    'status': 401
                }

            if method == "GET":
                response = {
                    'id': location.id,
                    'name': location.name,
                    'address': location.address,
                    'geolocation': location.geolocation,
                    'beacons': location.beacons,
                    'status': 200
                }
            elif method == "DELETE":
                location.delete()
                response = {
                    "message": "location {} deleted.".format(location.name),
                    'status': 200
                }
            elif method == "PUT":
                location.name = str(request.data.get('name', ''))
                address = str(request.data.get(
                    'address', '').encode('utf-8'))
                # Geocoding an address using gmaps service
                geocode_result = gmaps.geocode(address)
                location.address = geocode_result[0]['formatted_address']
                location.geolocation = geocode_result[0]['geometry']
                location.beacons = request.data.get('beacons','')
                location.save()

                response = {
                    'id': location.id,
                    'name': location.name,
                    'address': location.address,
                    'geolocation': location.geolocation,
                    'beacons' : location.beacons,
                    'status': 200
                }

            return response

        except Exception as e:
            # Create a response containing an string error message
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


class BeaconsLocationView(MethodView):
    def action(self, method, id):

        print("In beacons by location")
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
                for beacon in Beacon.query.filter_by(location_id=id).all():
                    obj = {
                        'id': beacon.id,
                        'role': beacon.role,
                        'major': beacon.major,
                        'minor': beacon.minor,
                        'identificator': beacon.identificator,
                        'name': beacon.name,
                        'status': beacon.status,
                        'location_id':beacon.location_id
                    }
                    response.append(obj)

            elif method == 'POST':
                post_data = request.data
                role = post_data['role']
                name = post_data['name']
                major = post_data['major']
                minor = post_data['minor']

                beacon = Beacon(role=role, name=name, major=major, minor=minor, location_id=id)

                beacon.save()

                beacons = []
                for beacon in Beacon.query.filter_by(location_id=id).all():
                    obj = {
                        'id': beacon.id,
                        'role': beacon.role,
                        'major': beacon.major,
                        'minor': beacon.minor,
                        'identificator': beacon.identificator,
                        'name': beacon.name,
                        'status': beacon.status,
                        'location_id':beacon.location_id
                    }
                    beacons.append(obj)

                response = {
                    'message': 'You registered Beacon ''{0}'' successfully.'.format(beacons[0].identificator),
                    'beacons': beacons,
                    'status': 201
                }

            return response

        except Exception as e:
            # Create a response containing an string error message
            return {
                'message': str(e),
                'status': 500
            }

    def get(self, id):
        response = self.action('GET', id)
        if 'status' in response:
            status = response['status']
            del response['status']
        else:
            status = 200

        return make_response(jsonify(response)), status

    def post(self, id):
        response = self.action('POST', id)
        if 'status' in response:
            status = response['status']
            del response['status']
        else:
            status = 200

        return make_response(jsonify(response)), status


class BeaconsView(MethodView):
    def action(self, method):

        print("In beacons")
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
                for beacon in Beacon.query.all():
                    obj = {
                        'id': beacon.id,
                        'role': beacon.role,
                        'major': beacon.major,
                        'minor': beacon.minor,
                        'identificator': beacon.identificator,
                        'name': beacon.name,
                        'status': beacon.status,
                        'location_id':beacon.location_id
                    }
                    response.append(obj)

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




locations_view = LocationsView.as_view('locations_view')
one_location_view = OneLocationVew.as_view('one_location_view')
beacons_view = BeaconsView.as_view('beacons_view')
beacons_location_view = BeaconsLocationViewView.as_view('beacons_location_view')

# GET
# Retrieves all locations that are within coordinates, if coordiantes are not provided then all locations are shown
# Parameters: lat and lng are optional, ?& parameters
# POST
# Saves a new location if not already exists
location_blueprint.add_url_rule(
    '/locations',
    view_func=locations_view,
    methods=['GET', 'POST'])

# GET
# Retrieves the location acording to the Location id
# PUT
# Updates the location acording to the Location id
# DELETE
# Deletes the location acording to the Location id
location_blueprint.add_url_rule(
    '/locations/<int:id>',
    view_func=one_location_view,
    methods=['GET', 'PUT', 'DELETE'])

# GET
# Retrieves all beacons of a Location
# POST
# Adds a Beacon to a Location
location_blueprint.add_url_rule(
    '/beacons/location/<int:id>',
    view_func=beacons_location_view,
    methods=['GET', 'POST'])

# GET
# Retrieves all beacons
location_blueprint.add_url_rule(
    '/beacons',
    view_func=beacons_view,
    methods=['GET'])
