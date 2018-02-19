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
                    'res-status': 400
                }
            access_token = auth_header.split(" ")[1]

            # Verify correct token
            if not access_token or isinstance(User.decode_token(access_token), str):
                # Attempt to decode the token and get the User ID
                return {
                    'message': "Authentication token error.",
                    'res-status': 511
                }

            response = {}
            if method == 'POST':

                if 'customer_id' in request.data:
                    customer_id = request.data['customer_id']
                else:
                    customer_id = User.decode_token(access_token)

                # Refactoring
                # agent_id = request.data['agent_id']
                location_id = request.data['location_id']
                auto_authorize = request.data['auto_authorize']
                expire = request.data['expire']
                options = request.data['options']

                from datetime import datetime, timedelta
                expire = datetime.utcnow() + timedelta(minutes=int(expire))

                # Refactoring
                contract = Contract.query.filter_by(customer_id=customer_id, location_id=location_id).first()
                    # customer_id=customer_id, agent_id=agent_id).first()

                # Refactoring
                if not contract:
                    contract = Contract(customer_id, location_id, auto_authorize, expire, options)
                        # customer_id, agent_id, auto_authorize, expire, options)
                    # print("step3")
                    contract.save()

                else:
                    contract.status = True
                    contract.expire = expire
                    contract.options = options
                    contract.auto_authorize = auto_authorize
                    contract.save()

                # Refactoring
                response = {
                    'message': 'Access from customer "{0}" to location "{1}" granted until {2}'.format(
                        contract.customer.name, contract.location.name, expire)
                        # contract.customer.name, contract.agent.name, expire, contract.agent.location.name)
                }

            return response

        except Exception as e:
            # Create a response containing an string error message
            response = {
                'message': str(e),
                'res-status': 500
            }
            # Return a server error using the HTTP Error Code 500 (Internal Server Error)

            return response

    def post(self):
        response = self.action('POST')
        if 'res-status' in response:
            status = response['res-status']
            del response['res-status']
        else:
            status = 200

        return make_response(jsonify(response)), status


class ContractOneView(MethodView):
    def action(self, method, location_id):

        from app.modules.users.models import User

        try:
            # Get the access token from the header
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return {
                    'message': "Token missing.",
                    'res-status': 400
                }
            access_token = auth_header.split(" ")[1]

            # Verify correct token
            if not access_token or isinstance(User.decode_token(access_token), str):
                # Attempt to decode the token and get the User ID
                return {
                    'message': "Authentication token error.",
                    'res-status': 511
                }

            customer_id = User.decode_token(access_token)

            response = {}

            contract = Contract.query.filter_by(location_id=location_id, customer_id=customer_id).first()

            if not contract or not contract.check_status():
                return {
                    'message': "No active contract",
                    'res-status': 404
                #     Area of improvement
                #     Could return a 200 status
                }

            if method == "GET":

                response = {
                    'customer_id': contract.customer_id,
                    'location_id': contract.location_id,
                    'status': contract.status,
                    'auto_authorize': contract.auto_authorize,
                    'expire': contract.expire,
                    'options': contract.options,
                    'res-status': 200
                }

            return response

        except Exception as e:
            # Create a response containing an string error message
            response = {
                'message': str(e.message),
                'res-status': 500
            }
            # Return a server error using the HTTP Error Code 500 (Internal Server Error)

            return response

    def get(self, id):
        response = self.action('GET', id)
        status = response['res-status']
        del response['res-status']

        return make_response(jsonify(response)), status


class ContractCustomersView(MethodView):
    def action(self, method, location_id):

        from app.modules.users.models import User

        try:
            # Get the access token from the header
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return {
                    'message': "Token missing.",
                    'res-status': 400
                }

            access_token = auth_header.split(" ")[1]

            # Verify correct token
            if not access_token or isinstance(User.decode_token(access_token), str):
                # Attempt to decode the token and get the User ID
                return {
                    'message': "Authentication token error.",
                    'res-status': 511
                }

            contracts = []

            # if method == 'POST':
            #     if 'customer_id' in request.data and 'location_id' in request.data:
            #         customer_id = request.data['customer_id']
            #         location_id = request.data['location_id']
            #         contracts = Contract.query.filter_by(customer_id=customer_id, location_id=location_id).all()
            #
            #     elif 'customer_id' in request.data:
            #         customer_id = request.data['customer_id']
            #         contracts = Contract.query.filter_by(customer_id=customer_id).all()
            #
            #     elif 'location_id' in request.data:
            #         location_id = request.data['location_id']
            #         contracts = Contract.query.filter_by(location_id=location_id).all()

            if method == "GET":
                contracts = Contract.query.filter_by(location_id=location_id).all()

            response = []

            from app.modules.users.models import Customer

            # Gathers the information of all the customers with an active contract by location
            for contract in contracts:
                if contract.check_status():

                    customer = Customer.query.filter_by(id=contract.customer_id).first()
                    obj = {
                        'customer_id': customer.id,
                        'customer_name': customer.name,
                        'customer_username': customer.username,
                        'customer_email': customer.email
                    }
                    response.append(obj)

            if len(response) == 0:
                response = {
                    'message': 'No active Contracts found.',
                    'res-status': 404
                #     Area of improvement
                #     Could return a 200 status
                }

            return response

        except Exception as e:
            # Create a response containing an string error message
            # Return a server error using the HTTP Error Code 500 (Internal Server Error)
            response = {
                'message': str(e),
                'res-status': 500
            }

            return response

    # def post(self):
    #     response = self.action('POST')
    #     if 'res-status' in response:
    #         status = response['res-status']
    #         del response['res-status']
    #     else:
    #         status = 200
    #
    #     return make_response(jsonify(response)), status

    def get(self, id):
        response = self.action('GET', id)
        if 'res-status' in response:
            status = response['res-status']
            del response['res-status']
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
                    'res-status': 400
                }

            access_token = auth_header.split(" ")[1]

            # Verify correct token
            if not access_token or isinstance(User.decode_token(access_token), str):
                # Attempt to decode the token and get the User ID
                return {
                    'message': "Authentication token error.",
                    'res-status': 511
                }

            contracts = []

            if method == 'POST':
                if 'customer_id' in request.data and 'location_id' in request.data:
                    customer_id = request.data['customer_id']
                    location_id = request.data['location_id']
                    contracts = Contract.query.filter_by(customer_id=customer_id, location_id=location_id).all()

                elif 'customer_id' in request.data:
                    customer_id = request.data['customer_id']
                    contracts = Contract.query.filter_by(customer_id=customer_id).all()

                elif 'location_id' in request.data:
                    location_id = request.data['location_id']
                    contracts = Contract.query.filter_by(location_id=location_id).all()

            if method == "GET":
                contracts = Contract.query.all()

            response = []

            from app.modules.users.models import Customer

            for contract in contracts:
                # print("b contract expire:"+str(contract.expire))
                # print("b contract status:"+ str(contract.status))
                if contract.check_status():
                    # print("a contract expire:" +str(contract.expire))
                    # print("a contract status:" + str(contract.status))

                    customer = Customer.query.filter_by(id=contract.customer_id).first()
                    obj = {
                        'customer_id': contract.customer_id,
                        'customer_name': customer.name,
                        'location_id': contract.location_id,
                        'status': contract.status,
                        'auto_authorize': contract.auto_authorize,
                        'expire': contract.expire,
                        'options': contract.options
                    }
                    response.append(obj)

            if len(response) == 0:
                response = {
                    'message': 'No active Contracts found.',
                    'res-status': 404
                #     Area of improvement
                #     Could return a 200 status
                }

            return response

        except Exception as e:
            # Create a response containing an string error message
            # Return a server error using the HTTP Error Code 500 (Internal Server Error)
            response = {
                'message': str(e),
                'res-status': 500
            }

            return response

    def post(self):
        response = self.action('POST')
        if 'res-status' in response:
            status = response['res-status']
            del response['res-status']
        else:
            status = 200

        return make_response(jsonify(response)), status

    def get(self):
        response = self.action('GET')
        if 'res-status' in response:
            status = response['res-status']
            del response['res-status']
        else:
            status = 200

        return make_response(jsonify(response)), status


class ContractExpireView(MethodView):
    def action(self, method):

        from app.modules.users.models import User

        try:
            # Get the access token from the header
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return {
                    'message': "Token missing.",
                    'res-status': 400
                }

            access_token = auth_header.split(" ")[1]

            # Verify correct token
            if not access_token or isinstance(User.decode_token(access_token), str):
                # Attempt to decode the token and get the User ID
                return {
                    'message': "Authentication token error.",
                    'res-status': 511
                }

            customer_id = request.data['customer_id']
            location_id = request.data['location_id']

            response = []

            if method == 'POST':

                contract = Contract.query.filter_by(customer_id=customer_id, location_id=location_id).first()

                if contract and contract.check_status():
                    contract.expireContract()
                    response = {
                        'message': 'Contract between {0} and location {1} expired.'.format(customer_id, location_id)
                    }
                else:
                    response = {
                        'message': 'No active Contract between {0} and location {1}'.format(customer_id, location_id),
                        'res-status': 404
                    #     Area of improvement
                    #     Could return a 200 status
                    }

            return response

        except Exception as e:
            # Create a response containing an string error message
            # Return a server error using the HTTP Error Code 500 (Internal Server Error)
            response = {
                'message': str(e),
                'res-status': 500
            }

            return response

    def post(self):
        response = self.action('POST')
        if 'res-status' in response:
            status = response['res-status']
            del response['res-status']
        else:
            status = 200

        return make_response(jsonify(response)), status


class ContractOptionsView(MethodView):
    def action(self, method):

        from app.modules.users.models import User

        try:
            # Get the access token from the header
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return {
                    'message': "Token missing.",
                    'res-status': 400
                }

            access_token = auth_header.split(" ")[1]

            # Verify correct token
            if not access_token or isinstance(User.decode_token(access_token), str):
                # Attempt to decode the token and get the User ID
                return {
                    'message': "Authentication token error.",
                    'res-status': 511
                }

            customer_id = request.data['customer_id']

            location_id = request.data['location_id']
            response = {}

            contract = Contract.query.filter_by(customer_id=customer_id, location_id=location_id).first()

            if not contract or not contract.check_status():
                return {
                        'message': 'No active Contract between {0} and location {1}'.format(customer_id, location_id),
                        'res-status': 404
                #     Area of improvement
                #     Could return a 200 status
                    }

            if method == 'POST':
                response = contract.options

            elif method == 'PATCH':
                contract.options = request.data['options']
                contract.save()

                response = {
                    'customer_id': contract.customer_id,
                    'location_id': contract.location_id,
                    'status': contract.status,
                    'auto_authorize': contract.auto_authorize,
                    'expire': contract.expire,
                    'options': contract.options
                }

            return response

        except Exception as e:
            # Create a response containing an string error message
            # Return a server error using the HTTP Error Code 500 (Internal Server Error)
            response = {
                'message': str(e),
                'res-status': 500
            }

            return response

    def post(self):
        response = self.action('POST')
        if 'res-status' in response:
            status = response['res-status']
            del response['res-status']
        else:
            status = 200

        return make_response(jsonify(response)), status

    def patch(self):
        response = self.action('PATCH')
        if 'res-status' in response:
            status = response['res-status']
            del response['res-status']
        else:
            status = 200

        return make_response(jsonify(response)), status


contract_view = ContractView.as_view('contract_view')
contract_one_view = ContractOneView.as_view('contract_one_view')
contract_customers_view = ContractCustomersView.as_view('contract_customer_view')
contract_active_view = ContractActiveView.as_view('contract_active_view')
contract_expire_view = ContractExpireView.as_view('contract_expire_view')
contract_options_view = ContractOptionsView.as_view('contract_options_view')

# POST
# Creates a new contract or updates the status of exiting one to Active
contract_blueprint.add_url_rule(
    '/contracts',
    view_func=contract_view,
    methods=['POST'])

# GET
# Retrieves a contract
# Parameters: Location id (from adress) and Customer id (from token)
contract_blueprint.add_url_rule(
    '/contracts/<int:id>',
    view_func=contract_one_view,
    methods=['GET'])

# GET
# Retrieves all customers with an active contract in a certain location
# Parameters: Location id
contract_blueprint.add_url_rule(
    '/contracts/customers/<int:id>',
    view_func=contract_customers_view,
    methods=['GET'])

# GET
# Retreives all active contracts
# POST
# Retreives all active contracts by Customer id and/or Location id
contract_blueprint.add_url_rule(
    '/contracts/active',
    view_func=contract_active_view,
    methods=['POST', 'GET'])

# Post
# Expires a contract between a Customer and a Location
contract_blueprint.add_url_rule(
    '/contracts/expire',
    view_func=contract_expire_view,
    methods=['POST'])

# POST
# Retreives the options of a contract between a Customer and a Location
# PATCH
# Updates the options of a contract between a Customer and a Location
contract_blueprint.add_url_rule(
    '/contracts/options',
    view_func=contract_options_view,
    methods=['POST', 'PATCH'])
