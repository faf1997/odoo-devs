from odoo import models, fields, api
from odoo.exceptions import ValidationError

class RepositoryPath(models.Model):
    _name = 'repository.path'
    _description = 'Repository Path'

    name = fields.Char(
        string='Path',
        required=True
        )
    
    active = fields.Boolean(
        string='Active',
        default=False
        )

    aux_repository_path = fields.Selection(
        [
        ('aux_path', '/home/odoo/tmp/aux_repository')
        ],
        default='aux_path'
        )

    @api.model
    def create(self, vals):
        record = super(RepositoryPath, self).create(vals)
        if record.active:
            self._set_only_one_active(record)
        return record


    def write(self, vals):
        if 'active' in vals and vals['active']:
            self._set_only_one_active(self)
        return super(RepositoryPath, self).write(vals)


    def _set_only_one_active(self, current_record):
        active_records = self.search([('active', '=', True), ('id', '!=', current_record.id)])
        if active_records:
            active_records.write({'active': False})

