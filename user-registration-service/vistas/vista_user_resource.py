from flask_restful import Api, Resource, reqparse
from failures_with_user_registration_log import registrar_falla_en_registro
from user_registration_service_principal import registrar_usuario_principal
import datetime
import requests

class UserResource(Resource):

    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('email', type=str, required=True, help='Email address is required')
            parser.add_argument('simulate_failure', type=bool, required=False)
            parser.add_argument('failure_uuid', type=str, required=False)
            args = parser.parse_args()
            email = args['email']
            
            search_url = 'http://127.0.0.1:6000/api/v1/search'
            params = {'email': email}
            response = requests.get(search_url, params=params)
            
            if response.status_code == 200 and response.json().get('status') == 'success':
                return {'status': 'error', 'message': 'Email already exists'}, 500
            
            if 'simulate_failure' in args and args['simulate_failure']==True:
                failure_uuid = args['failure_uuid']
                failure_datetime = str(datetime.datetime.now())
                raise Exception(str(failure_uuid) + ";" + email + ";" + str(failure_datetime))

            registrar_usuario_principal.delay(email)

        except Exception as e:
            error_message = str(e)
            registrar_falla_en_registro.delay(error_message)
            return {
                'status':'success', 
                'message': ('Email received successfully. We are experiencing latencies '
                            'but we received your email and we will register you.')
            }, 200

        return {'status':'success', 'message': 'Email received successfully'}, 200