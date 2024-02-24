from flask_restful import Resource, reqparse
from failures_search_user_log import registrar_falla_en_busqueda
from search_service_log import buscar_email_recibido
from flask import request
import datetime

class SearchResource(Resource):
    def get(self):
        search_datetime = str(datetime.datetime.now())
        email = request.args.get('email', type=str)

        if not email:
            return {'status': 'error', 'message': 'Email parameter is missing'}, 400

        try:
            task = buscar_email_recibido.delay(email=email)
            result = task.get(timeout=10) 

            if result:
                return {
                    'status': 'success',
                    'message': 'Email found',
                    "email": email,
                    'result': result,
                    "search_datetime": search_datetime
                }, 200
            else:
                # return {'status': 'error', 'message': f"Email {email} not found"}, 404
                raise Exception(str('') + "" + email + ";" + str(search_datetime))

        except Exception as e:
            registrar_falla_en_busqueda.delay(str(e))
            return {
                'status': 'error',
                'message': 'No se ha encontrado el email en la base de datos.',
                'error_message': str(e),
                'email': email,
                'search_datetime': search_datetime
            }, 200
