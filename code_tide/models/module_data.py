from odoo import models, fields, api, tools, _
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)


class ModuleData(models.Model):
    _name = 'module.data'
    _description = 'Data Modules'


    name = fields.Char(
        string='Name',
        readonly=True
    )

    email = fields.Char(
        string='Email',
        readonly=True
    )

    commit_description = fields.Char(
        string='Commit description',
        readonly=True
    )

    hash = fields.Char(
        string='Hash',
        unique=True,
        readonly=True
    )

    path_submodules = fields.Char(
        string='Path submodules',
        readonly=True
    )

    date = fields.Date(
        string='Date commit',
        readonly=True
    )

    is_submodule = fields.Boolean(
        string='Is submodule?',
        readonly=True
    )

    submodules = fields.Many2many(
        comodel_name='module.data',
        relation='module_data_submodules_rel',  # Nombre de la tabla relacional
        column1='module_id',  # Nombre de la columna en la tabla relacional que referenciará a este modelo
        column2='submodule_id',  # Nombre de la columna en la tabla relacional que referenciará a los submódulos
    )

    remote_ssh = fields.Char(
        string='URL remote',
        readonly=True
    )


    odoo_version = fields.Char(
        string='Odoo version',
        readonly=True
    )


