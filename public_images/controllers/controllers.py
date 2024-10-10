from odoo import http
from odoo.http import request
import base64

class PublicImageController(http.Controller):

    @http.route('/public_image/<int:product_id>/<string:field>', type='http', auth='public', website=True)
    def public_image(self, product_id, field, **kwargs):
        # Buscar el producto utilizando el product_id
        product = request.env['product.template'].sudo().browse(product_id)
        
        if product.exists() and hasattr(product, field):
            # Obtener la imagen en base64 y decodificarla
            image_content = getattr(product, field)
            if image_content:
                image_content = base64.b64decode(image_content)
                headers = [('Content-Type', 'image/jpeg')]
                return request.make_response(image_content, headers)
        
        return request.not_found()
