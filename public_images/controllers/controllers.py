from odoo import http, models, fields
from odoo.http import request
import base64



class ProductTemplate(models.Model):
    _inherit = 'product.template'

    public_link  = fields.Char(string='Public link', compute='_compute_link')
    old_ref = fields.Integer(string='Old Reference', compute='_compute_old_ref')


    def _compute_link(self):
        for product in self:
            if product.image_1024:
                product.public_link = +'https://geminis.ntsystemwork.com.ar/en/public_image/' + str(product.id) +'/image_1024'


    def _compute_old_ref(self):
        for product in self:
            product.old_ref = product.id




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
