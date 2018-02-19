from flask import make_response, request, jsonify
from flask.views import MethodView

from app.modules.companies.models import Company
from . import company_blueprint


class CompaniesView(MethodView):

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

                companies = Company.query.all()

                for company in companies:
                    obj = {
                        'id': company.id,
                        'name': company.name,
                        'code': company.code,
                        'agents_left': company.agents_left
                    }
                    response.append(obj)

            elif method == 'POST':

                # Query to see if the user already exists
                post_data = request.data
                # Register the location
                name = post_data['name']
                code = post_data['code']
                agents_left = post_data['agents_left']

                company = Company.query.filter_by(name=name).first()

                if company:
                    return {
                        'message': 'Company already exists. Please use a different name.',
                        'status': 202
                    }

                company = Company(name=name, code=code, agents_left=agents_left)

                company.save()

                response = {
                    'message': 'You registered Company ''{0}'' successfully.'.format(company.name),
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


class OneCompanyVew(MethodView):
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

            company = Company.query.filter_by(id=id).first()

            if not company:
                return {
                    'message': "Company does not exist.",
                    'status': 401
                }

            if method == "GET":
                response = {
                    'id': company.id,
                    'name': company.name,
                    'code': company.code,
                    'agents_left': company.agents_left,
                    'status': 200
                }
            elif method == "DELETE":
                company.delete()
                response = {
                    "message": "Company {} deleted.".format(company.name),
                    'status': 200
                }
            elif method == "PUT":
                company.name = str(request.data.get('name', ''))
                company.code = str(request.data.get('code', ''))
                company.agents_left = str(request.data.get('agents_left', ''))
                company.save()

                response = {
                    'id': company.id,
                    'name': company.name,
                    'code': company.code,
                    'agents_left': company.agents_left,
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


companies_view = CompaniesView.as_view('companies_view')
one_company_view = OneCompanyVew.as_view('one_company_view')

# GET
# Retrieves all companies
# POST
# Saves a new company
company_blueprint.add_url_rule(
    '/companies',
    view_func=companies_view,
    methods=['GET', 'POST'])

# GET
# Retrieves an specific company depending on the company id
# PUT
# Updates an specific company depending on the company id
# DELETE
# Deletes an specific company depending on the company id
company_blueprint.add_url_rule(
    '/companies/<int:id>',
    view_func=one_company_view,
    methods=['GET', 'PUT', 'DELETE'])
