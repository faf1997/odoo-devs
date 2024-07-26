from odoo import models, fields

class ModuleTracking(models.Model):
    _name = 'module.tracking'
    _description = 'Module Tracking'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')