from flask import make_response, request, jsonify
from flask.views import MethodView

from app.modules.contracts.models import Contract
from . import contract_blueprint


class ContractView(MethodView):
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

            if method == 'POST':

                customer_id = request.data['customer_id']
                agent_id = request.data['agent_id']
                auto_authorize = request.data['auto_authorize']
                expire = request.data['expire']

                from datetime import datetime, timedelta
                expire = datetime.utcnow() + timedelta(minutes=int(expire))

                contract = Contract.query.filter_by(
                    customer_id=customer_id, agent_id=agent_id).first()

                if not contract:
                    contract = Contract(
                        customer_id, agent_id, auto_authorize, expire)
                    contract.save()

                else:
                    contract.status = True
                    contract.expire = expire
                    contract.auto_authorize = auto_authorize
                    contract.save()

                response = {
                    'message': 'Access from {0} to {1} in location {3} granted until {2}'
                        .format(contract.customer.name, contract.agent.name, expire, contract.agent.location.name)
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

    def post(self):
        response = self.action('POST')
        if 'status' in response:
            status = response['status']
            del response['status']
        else:
            status = 200

        return make_response(jsonify(response)), status


class ContractActiveView(MethodView):
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

            if method == 'POST':
                customer_id = request.data['customer_id']
                if 'agent_id' in request.data:
                    agent_id = request.data['agent_id']
                elif 'location_id' in request.data:
                    location_id = request.data['location_id']

                    from app.modules.locations.models import Location
                    location = Location.query.get(location_id)
                    agents = location.get_agents_in_location()

                    agent_id = 0
                    for agent in agents:
                        if Contract.query.filter_by(customer_id=customer_id, agent_id=agent.id).first():
                            agent_id = agent.id

                else:
                    return {
                            'message': "Agent id or Location id missing.",
                            'status': 400
                        }

                contract = Contract.query.filter_by(customer_id=customer_id, agent_id=agent_id).first()
                response = []

                if contract and contract.check_expire():
                    obj = {
                        'customer_id': contract.customer_id,
                        'agent_id': contract.agent_id,
                        'status': contract.status,
                        'auto_authorize': contract.auto_authorize,
                        'expire': contract.expire
                    }
                    response.append(obj)
                else:
                    response = {
                        'message': 'No active Contract between {0} and {1}'
                        .format(customer_id, agent_id)
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

    def post(self):
        response = self.action('POST')
        if 'status' in response:
            status = response['status']
            del response['status']
        else:
            status = 200

        return make_response(jsonify(response)), status


contract_view = ContractView.as_view('contract_view')
contract_active_view = ContractActiveView.as_view('contract_active_view')

contract_blueprint.add_url_rule(
    '/contracts',
    view_func=contract_view,
    methods=['POST'])

contract_blueprint.add_url_rule(
    '/contracts/active',
    view_func=contract_active_view,
    methods=['POST'])
