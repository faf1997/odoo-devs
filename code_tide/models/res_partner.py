from odoo import fields, models




class ResPartner(models.Model):
    _inherit = 'res.partner'


    git_repository = fields.Char(string='Repositorio ssh')
