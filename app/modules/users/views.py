# /app/modules/users/views.py
import googlemaps
from flask import make_response, request, jsonify
from flask.views import MethodView

import instance.config as config
from app.modules.locations.models import Location
from app.modules.users.models import Agent
from . import users_blueprint

google_api_key = config.Config.GOOGLE_API_KEY

gmaps = googlemaps.Client(key=google_api_key)


# inactive class
class AgentsView(MethodView):
    def action(self, method):

        from app.modules.users.models import User
        from app.modules.contracts.models import Contract

        try:
            # Get the access token from the header
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return {
                    'message': "Token missing.",
                    'status': 511
                }
            access_token = auth_header.split(" ")[1]

            # Verify correct token
            if not access_token or isinstance(User.decode_token(access_token), str):
                # Attempt to decode the token and get the User ID
                return {
                    'message': "Authentication token error.",
                    'status': 511
                }

            if method == "GET":

                # Return only the list of location matching the coordinates on the UR
                lat = request.args.get('lat')
                lng = request.args.get('lng')

                locations = Location.query.all()
                # locations = Location.query.filter(Location.address != 'mobile').all()

                # Gets rid off mobile locations
                locations = [l for l in locations if l.address != 'mobile']

                response = []

                if not lat or not lng:
                    return {
                        'message': 'Please provide lat and lng.',
                        'status': 400
                    }

                for location in locations:
                    # print("address: "+location.address)
                    lat = float(lat)
                    lng = float(lng)
                    latne = float(
                        location.geolocation['bounds']['northeast']['lat'])
                    lngne = float(
                        location.geolocation['bounds']['northeast']['lng'])
                    latsw = float(
                        location.geolocation['bounds']['southwest']['lat'])
                    lngsw = float(
                        location.geolocation['bounds']['southwest']['lng'])

                    # print (location.name + str(latne) +'>='+ str(lat)+' '+str(lngne) +'>='+ str(lng)+' '
                    #        +str(latsw) +'<='+ str(lat) +' '+ str(lngsw) +'<='+ str(lng))

                    if (latne >= lat and lngne >= lng) and (latsw <= lat and lngsw <= lng):
                        print("entro con location: " + str(location.id))
                        agents = Agent.query.filter_by(location_id=location.id).all()
                        print ("agents len: "+str(len(agents)))
                        if agents:
                            for agent in agents:
                                customer_id = request.args.get('customer_id')
                                #
                                print("args: "+str(len(request.args)))
                                # print("current: "+current)

                                # TODO return only non-contracts agents

                                # return all agents in my location with expired contracts or nonexistant
                                if customer_id:
                                    print("torm")
                                    contract = Contract.query.filter_by(
                                        agent_id=agent.id, customer_id=customer_id).first()

                                    if not contract or not contract.check_status():
                                        obj = {
                                            'id': agent.id,
                                            'name': agent.name,
                                            'location_id': agent.location_id,
                                            'location_name': agent.location.name
                                        }
                                        response.append(obj)

                                # returns all agents in my location
                                else:
                                    obj = {
                                        'id': agent.id,
                                        'name': agent.name,
                                        'location_id': agent.location_id,
                                        'location_name': agent.location.name
                                    }
                                    response.append(obj)

                    if not response:
                        response = {
                            'message': 'No agents in that location',
                            'status': 200
                            # 'status': 204 # no content
                        }

                return response

        except Exception as e:
            # Create a response containing an string error message
            response = {
                'message': str(e),
                'status': 500
            }
            # Return a server error using the HTTP Error Code 500 (Internal Server Error)

            return response
            # return make_response(jsonify(response)), 500

    def get(self):
        response = self.action('GET')
        if 'status' in response:
            status = response['status']
            del response['status']
        else:
            status = 200

        return make_response(jsonify(response)), status


class AgentsMobileView(MethodView):
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

            # Verify correct token
            if not access_token or isinstance(User.decode_token(access_token), str):
                # Attempt to decode the token and get the User ID
                return {
                    'message': "Authentication token error.",
                    'status': 511
                }

            if method == "GET":

                response = []

                location_id = Location.query.filter_by(address='mobile').first().id

                agents = Agent.query.filter_by(
                    location_id=location_id).all()

                if agents:
                    for agent in agents:
                        obj = {
                            'id': agent.id,
                            'name': agent.name,
                            'location_id': agent.location_id,
                            'location_name': agent.location.name
                        }
                        response.append(obj)

                    if not response:
                        response = {
                            'message': 'No agents are mobile.',
                            'status': 200
                        }

                else:
                    response = {
                        'message': 'No agents are mobile.',
                        'status': 200
                    }

                return response


        except Exception as e:
            # Create a response containing an string error message
            response = {
                'message': str(e),
                'status': 500
            }
            # Return a server error using the HTTP Error Code 500 (Internal Server Error)

            return response
            # return make_response(jsonify(response)), 500

    def get(self):
        response = self.action('GET')
        if 'status' in response:
            status = response['status']
            del response['status']
        else:
            status = 200

        return make_response(jsonify(response)), status


agents_view = AgentsView.as_view('agents_view')
agents_mobile_view = AgentsMobileView.as_view('agents_mobile_view')

# TODO crate a service to return all customers in same location as agent
# customers_view = CustomersView.as_view('customers_view')

# users_blueprint.add_url_rule(
#     '/agents',
#     view_func=agents_view,
#     methods=['GET'])

users_blueprint.add_url_rule(
    '/agents/mobile',
    view_func=agents_mobile_view,
    methods=['GET'])
