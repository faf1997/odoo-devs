# from odoo import http
# from odoo.http import request
# import json

# class GenericController(http.Controller):
#     @http.route('/generic/json', type='json', auth='public', methods=['POST'], csrf=False)
#     def handle_json(self, **kwargs):
#         try:
#             # kwargs ya contiene el JSON enviado
#             data = kwargs
#             # Procesar el JSON aquí
#             return {
#                 'status': 'success',
#                 'message': 'JSON recibido correctamente',
#                 'data': data
#             }
#         except Exception as e:
#             return {
#                 'status': 'error',
#                 'message': str(e)
#             }
            
            
# from odoo import http
# from odoo.http import request
# import json

# class CustomController(http.Controller):

#     @http.route('/custom_route', auth='public', type='json', methods=['POST'], csrf=False)
#     def handle_json_request(self, **post):
#         incoming_json = request.jsonrequest  # Obtener el JSON de la solicitud entrante
#         # Aquí puedes procesar los datos del JSON recibido como lo necesites

#         # Ejemplo de creación de un JSON de respuesta
#         response_json = {
#             'message': 'Solicitud recibida con éxito',
#             'data': incoming_json
#         }

#         return json.dumps(response_json)



# from odoo import http
# from odoo.http import request

# class CustomController(http.Controller):

#     @http.route('/custom_route', auth='public', type='json', methods=['POST'], csrf=False)
#     def handle_json_request(self, **post):
#         incoming_json = request.jsonrequest  # Obtener el JSON de la solicitud entrante
#         # Aquí puedes procesar los datos del JSON recibido como lo necesites

#         # Ejemplo de creación de un JSON de respuesta
#         response_json = {
#             'message': 'Solicitud recibida con éxito',
#             'data': incoming_json
#         }

#         return response_json



import re
import subprocess
from odoo import http
from odoo.http import request

import logging




_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)



def is_github_ssh_link(url):
    pattern = r'^git@github\.com:.*\.git$'
    return bool(re.match(pattern, url))


def get_odoo_major_version(version_str):
    match = re.search(r'\b\d+\.\d+\b', version_str)
    return match.group() if match else None




class CustomController(http.Controller):
    
    @http.route('/code_tide_server', auth='public', type='json', methods=['GET','POST'], csrf=False)
    def custom_route(self, **post):
        self.print_data(post)
        response_json = {
            'message': 'Solicitud recibida con éxito'
        }
        return response_json


    def print_data(self, data):
        _logger.warning('\n')
        for key in data:
            _logger.warning(f'{key}: {data[key]}')
        _logger.warning('\n')