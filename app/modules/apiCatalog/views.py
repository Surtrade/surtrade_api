from flask import make_response, request, jsonify
from flask.views import MethodView
from datetime import datetime

from app.modules.apiCatalog.models import ApiCatalog
from . import apiCatalog_blueprint


class ApiCatalogView(MethodView):

    def action(self, method):

        from app.modules.users.models import User

        try:
            # Get the access token from the header
            # auth_header = request.headers.get('Authorization')
            # if not auth_header:
            #     return {
            #         'message': "Token missing.",
            #         'status': 400
            #     }
            # access_token = auth_header.split(" ")[1]
            #
            # if not access_token or isinstance(User.decode_token(access_token), str):
            #     # Attempt to decode the token and get the User ID
            #     return {
            #         'message': "Authentication token error.",
            #         'status': 511
            #     }

            response = []

            if method == "GET":
                print("gimme the services 1")
                services = ApiCatalog.query.all()
                print("da services: "+ str(services))
                for service in services:
                    print("da service: " + str(service))
                    print('method type: '+ str(type(service.method)))
                    obj = {
                        'id': service.id,
                        'name': service.name,
                        'method': service.method.value,
                        'url': service.url,
                        'description': service.description,
                        'details': service.details,
                        'security_level': service.security_level.value,
                        'security_level_name': service.security_level.name,
                        'last_modified': service.last_modified
                    }
                    response.append(obj)

            elif method == 'POST':

                post_data = request.data
                name = post_data['name']
                method = post_data['method']
                url = post_data['url']
                description = post_data['description']
                details = post_data['details']
                security_level = post_data['security_level']


                service = ApiCatalog.query.filter_by(name=name).first()

                if service:
                    return {
                        'message': 'Service already exists. Please use a different name.',
                        'status': 202
                    }

                service = ApiCatalog(name=name, method=method, url=url, description=description, details=details,
                                     security_level=security_level)

                service.save()

                response = {
                    'message': 'You registered Service ''{0}'' successfully.'.format(service.name),
                    'status': 201
                }

            print("gimme the services 2")
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


# TODO remove: used for sessions dummy data
class SessionsView(MethodView):

    def action(self, method):

        try:

            response = []

            if method == "GET":
                response = [
                    {
                        'id': '1',
                        'title': 'Session 1',
                        'start': '2016-10-03T12:00:00Z',
                        'end': '2016-10-03T13:00:00Z',
                        'room': 'room1',
                        'roomInfo': {
                            'roomId': 'room1',
                            'name': 'Myroom1',
                            'url': 'http://google.com',
                            'theme': ''
                        },
                        'speakers': [
                            {
                                'id': '1',
                                'name': 'Speaker 1',
                                'company': 'Company 1',
                                'picture': '',
                                'twitterName': '@Speaker1'
                            },
                            {
                                'id': '2',
                                'name': 'Speaker 2',
                                'company': 'Company 1',
                                'picture': '',
                                'twitterName': '@Speaker2'
                            }
                        ],
                        'description': 'Session 1 desc',
                        'descriptionShort': 'Session 1 short desc',
                        'calendarEventId': '',
                        'isBreak': False
                    },
                    {
                        'id': '2',
                        'title': 'Session 2',
                        'start': '2016-10-04T13:00:00Z',
                        'end': '2016-10-04T14:00:00Z',
                        'room': 'room2',
                        'roomInfo': {
                            'roomId': 'room2',
                            'name': 'Myroom2',
                            'url': 'http://google.com',
                            'theme': ''
                        },
                        'speakers': [
                            {
                                'id': '3',
                                'name': 'Speaker 3',
                                'company': 'Company 2',
                                'picture': '',
                                'twitterName': '@Speaker3'
                            },
                            {
                                'id': '4',
                                'name': 'Speaker 4',
                                'company': 'Company 2',
                                'picture': '',
                                'twitterName': '@Speaker4'
                            }
                        ],
                        'description': 'Session 2 desc',
                        'descriptionShort': 'Session 2 short desc',
                        'calendarEventId': '',
                        'isBreak': False
                    },
                    {
                        'id': '3',
                        'title': 'Session 3',
                        'start': '2016-10-05T15:00:00Z',
                        'end': '2016-10-05T16:00:00Z',
                        'room': 'room3',
                        'roomInfo': {
                            'roomId': 'room3',
                            'name': 'Myroom3',
                            'url': 'http://google.com',
                            'theme': ''
                        },
                        'speakers': [
                            {
                                'id': '1',
                                'name': 'Speaker 1',
                                'company': 'Company 1',
                                'picture': '',
                                'twitterName': '@Speaker1'
                            },
                            {
                                'id': '3',
                                'name': 'Speaker 3',
                                'company': 'Company 2',
                                'picture': '',
                                'twitterName': '@Speaker3'
                            },
                            {
                                'id': '4',
                                'name': 'Speaker 4',
                                'company': 'Company 2',
                                'picture': '',
                                'twitterName': '@Speaker4'
                            }
                        ],
                        'description': 'Session 3 desc',
                        'descriptionShort': 'Session 3 short desc',
                        'calendarEventId': '',
                        'isBreak': False
                    },
                    {
                        'id': '4',
                        'title': 'Break 1',
                        'start': '2016-10-03T14:00:00Z',
                        'end': '2016-10-03T15:00:00Z',
                        'room': '',
                        'roomInfo': 'null',
                        'speakers': [],
                        'description': '',
                        'descriptionShort': '',
                        'calendarEventId': '',
                        'isBreak': True
                    }
                ]

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


class OneApiCatalogVew(MethodView):
    def action(self, method, id):
        from app.modules.users.models import User

        try:
            # Get the access token from the header
            # auth_header = request.headers.get('Authorization')
            # if not auth_header:
            #     return {
            #         'message': "Token missing.",
            #         'status': 400
            #     }
            #
            # access_token = auth_header.split(" ")[1]
            #
            # # Verify correct token
            # if not access_token or isinstance(User.decode_token(access_token), str):
            #     # Attempt to decode the token and get the User ID
            #     return {
            #         'message': "Authentication token error.",
            #         'status': 511
            #     }

            response = {}

            service = ApiCatalog.query.filter_by(id=id).first()

            if not service:
                return {
                    'message': "Service does not exist.",
                    'status': 401
                }

            if method == "GET":
                response = {
                    'id': service.id,
                    'name': service.name,
                    'method': service.method.value,
                    'url': service.url,
                    'description': service.description,
                    'details': service.details,
                    'security_level': service.security_level.value,
                    'security_level_name': service.security_level.name,
                    'last_modified': service.last_modified,
                    'status': 200
                    }
            elif method == "DELETE":
                service.delete()
                response = {
                    "message": "Service {} deleted.".format(service.name),
                    'status': 200
                }
            elif method == "PUT":
                service.name = str(request.data.get('name', ''))
                service.method = str(request.data.get('method', ''))
                service.url = str(request.data.get('url', ''))
                service.description = str(request.data.get('description', ''))
                service.details = str(request.data.get('details', ''))
                service.security_level = str(request.data.get('security_level', ''))
                service.last_modified = datetime.utcnow()
                service.save()

                response = {
                    'id': service.id,
                    'name': service.name,
                    'method': service.method,
                    'url': service.url,
                    'description': service.description,
                    'details': service.details,
                    'security_level': service.security_level,
                    'last_modified': service.last_modified,
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


apiCatalog_view = ApiCatalogView.as_view('apiCatalogs_view')
one_apiCatalog_view = OneApiCatalogVew.as_view('one_apiCatalog_view')

# TODO remove: used for sessions dummy data
sessions_view = SessionsView.as_view('sessions_view')

apiCatalog_blueprint.add_url_rule(
    '/services',
    view_func=apiCatalog_view,
    methods=['GET', 'POST'])

apiCatalog_blueprint.add_url_rule(
    '/services/<int:id>',
    view_func=one_apiCatalog_view,
    methods=['GET', 'PUT', 'DELETE'])


# TODO remove: used for sessions dummy data
apiCatalog_blueprint.add_url_rule(
    '/sessions',
    view_func=sessions_view,
    methods=['GET'])
