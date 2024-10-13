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
        
        
        
        
class ProductImageController(http.Controller):

    @http.route('/product_image/<model("product.template"):product>', type='http', auth='public', website=True)
    def product_image(self, product, **kwargs):
        if product.image_512:
            image_content = product.image_128
            headers = [('Content-Type', 'image/jpeg')]
            return request.make_response(image_content, headers)
        
        return request.not_found()
    
