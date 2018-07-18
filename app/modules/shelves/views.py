from flask import make_response, request, jsonify
from flask.views import MethodView
import json

from app.modules.shelves.models import Shelf, Product
from app.modules.shelves import shelf_blueprint, product_blueprint


class ShelvesView(MethodView):

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

                shelves = Shelf.query.all()


                for shelf in shelves:
                    products = []
                    for p in shelf.products:
                        products.append({"name":p.name,"code":p.code,"description":p.description,"keywords":p.keywords,"image":p.image})
                    obj = {
                        'id': shelf.id,
                        'code': shelf.code,
                        'beacon': shelf.beacon,
                        'products': products,
                        'created_dt': shelf.created_dt,
                        'active': shelf.active,
                        'keywords': shelf.keywords
                    }

                    response.append(obj)


            elif method == 'POST':
                # Query to see if the shelf already exists
                post_data = request.data

                code = post_data['code']
                beacon = post_data['beacon']
                keywords = post_data['keywords']
                products = post_data['products']

                currentShelf = Shelf.query.filter_by(beacon=beacon,active=True).first()
                if currentShelf:
                    print("Deactivating shelf with id ",currentShelf.id)
                    currentShelf.active = False
                    currentShelf.save()

                shelf = Shelf(code, beacon)

                shelf.active = True
                shelf.keywords = keywords

                for product_id in products:
                    product = Product.query.filter_by(id=product_id).first()
                    if (product):
                        shelf.products.append(product)

                shelf.save()

                response = {
                    'message': 'You registered Shelf ''{0}'' to beacon ''{1}'' successfully.'.format(shelf.code, shelf.beacon),
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


class OneShelfView(MethodView):
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

            shelf = Shelf.query.filter_by(id=id).first()

            if not shelf:
                return {
                    'message': "Shelf does not exist.",
                    'status': 401
                }

            if method == "GET":
                response = {
                    'id': shelf.id,
                    'code': shelf.code,
                    'beacon': shelf.beacon,
                    'active': shelf.active,
                    'keywords': shelf.keywords,
                    'status': 200
                }
            elif method == "DELETE":
                shelf.delete()
                response = {
                    "message": "Shelf  ''{0}'' with beacon ''{1}'' was deleted.".format(shelf.code, shelf.beacon),
                    'status': 200
                }
            elif method == "PUT":
                shelf.code = str(request.data.get('code', ''))
                shelf.beacon = str(request.data.get('beacon', ''))
                shelf.active = str(request.data.get('active', ''))
                shelf.keywords = str(request.data.get('keywords', ''))

                shelf.save()

                response = {
                    'id': shelf.id,
                    'code': shelf.code,
                    'beacon': shelf.beacon,
                    'active': shelf.active,
                    'keywords': shelf.keywords,
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


class OneShelfByBeaconView(MethodView):
    def action(self, method, beacon):
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

            shelf = Shelf.query.filter_by(beacon=beacon, active=True).first()

            if not shelf:
                return {
                    'message': "Shelf does not exist.",
                    'status': 401
                }

            if method == "GET":
                products = []
                for p in shelf.products:
                    products.append(
                        {"name": p.name, "code": p.code, "description": p.description, "keywords": p.keywords, "image":p.image})
                response = {
                    'id': shelf.id,
                    'code': shelf.code,
                    'beacon': shelf.beacon,
                    'products': products,
                    'created_dt': shelf.created_dt,
                    'active': shelf.active,
                    'keywords': shelf.keywords,
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

    def get(self, beacon):
        response = self.action('GET', beacon)
        status = response['status']
        del response['status']

        return make_response(jsonify(response)), status


class ProductsView(MethodView):

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

                products = Product.query.all()

                for product in products:
                    obj = {
                        'id': product.id,
                        'code': product.code,
                        'name': product.name,
                        'description': product.description,
                        'keywords': product.keywords,
                        'image': product.image,
                    }
                    response.append(obj)

            elif method == 'POST':

                # Query to see if the product already exists
                post_data = request.data

                code = post_data['code']
                name = post_data['name']
                description = post_data['description']
                keywords = post_data['keywords']
                image = post_data['image']

                product = Product(code, name, description)

                product.keywords = keywords
                product.image = image

                product.save()

                response = {
                    'message': 'You registered Product ''{0}'' successfully.'.format(product.name),
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


class OneProductView(MethodView):
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

            product = Product.query.filter_by(id=id).first()

            if not product:
                return {
                    'message': "Product does not exist.",
                    'status': 401
                }

            if method == "GET":
                response = {
                    'id': product.id,
                    'code': product.code,
                    'name': product.name,
                    'description': product.description,
                    'keywords': product.keywords,
                    'image': product.image,
                    'status': 200
                }
            elif method == "DELETE":
                product.delete()
                response = {
                    "message": "Product  ''{0}'' was deleted.".format(product.name),
                    'status': 200
                }
            elif method == "PUT":
                product.code = str(request.data.get('code', ''))
                product.name = str(request.data.get('name', ''))
                product.description = str(request.data.get('description', ''))
                product.keywords = request.data.get('keywords', '')
                product.image = str(request.data.get('image', ''))

                product.save()

                response = {
                    'id': product.id,
                    'code': product.code,
                    'name': product.name,
                    'description': product.description,
                    'keywords': product.keywords,
                    'image': product.image,
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


shelves_view = ShelvesView.as_view('shelves_view')
one_shelf_view = OneShelfView.as_view('one_shelf_view')
one_shelf_by_beacon_view = OneShelfByBeaconView.as_view('one_shelf_by_beacon_view')

products_view = ProductsView.as_view('products_view')
one_product_view = OneProductView.as_view('one_product_view')

# GET
# Retrieves all shelves
# POST
# Saves a new shelf
shelf_blueprint.add_url_rule(
    '/shelves',
    view_func=shelves_view,
    methods=['GET', 'POST'])

# GET
# Retrieves an specific shelf depending on the shelf id
# PUT
# Updates an specific shelf depending on the shelf id
# DELETE
# Deletes an specific shelf depending on the shelf id
shelf_blueprint.add_url_rule(
    '/shelves/<int:id>',
    view_func=one_shelf_view,
    methods=['GET', 'PUT', 'DELETE'])

# GET
# Retrieves an specific shelf depending on the beacon
shelf_blueprint.add_url_rule(
    '/shelves/beacon/<string:beacon>',
    view_func=one_shelf_by_beacon_view,
    methods=['GET'])

# GET
# Retrieves all products
# POST
# Saves a new product
product_blueprint.add_url_rule(
    '/products',
    view_func=products_view,
    methods=['GET', 'POST'])

# GET
# Retrieves an specific product depending on the product id
# PUT
# Updates an specific product depending on the product id
# DELETE
# Deletes an specific product depending on the product id
product_blueprint.add_url_rule(
    '/products/<int:id>',
    view_func=one_product_view,
    methods=['GET', 'PUT', 'DELETE'])
