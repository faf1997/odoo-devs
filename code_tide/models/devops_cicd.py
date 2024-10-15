from odoo import models, fields, api, tools, _
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)


class DevopsCicd(models.Model):
    _name = 'devops.cicd'
    _description = 'Continuous Integration and Continuous Delivery'


    name = fields.Char(
        string='Name',
    )

    date_start = fields.Datetime(
        string='Start Date',
        # required=True
    )

    date_end = fields.Datetime(
        string='End Date',
        # required=True
    )

    task_id = fields.Many2one(
        comodel_name='project.task',
        string='Task'
    )
    
    customer_id = fields.Many2one(
        comodel_name='res.partner',
        string='Customer',
    )

    functional = fields.Many2one(
       comodel_name='res.users',
        string='Functional',
    )
    
    repository_name = fields.Char(
        string='Repository Name',
    )
    
    module_name = fields.Many2one(
        comodel_name='module.data',
        string='Module',
    )
    
    description = fields.Char(
        string='Description',
    )
    
    indirectly_updated_modules = fields.Many2many(
        'module.data',
        string='Indirectly updated modules',
    )

    indirectly_updated_modules = fields.Many2many(
        comodel_name='module.data',
        relation='module_data_submodules_cicd_rel',  # Nombre de la tabla relacional
        column1='module_id',  # Nombre de la columna en la tabla relacional que referenciará a este modelo
        column2='submodule_id',  # Nombre de la columna en la tabla relacional que referenciará a los submódulos
    )

    devops_in_charge = fields.Many2one(
        comodel_name='res.users',
        string='DevOps in charge',
    )
    
    dev_in_charge = fields.Many2one(
        comodel_name='res.users',
        string='Dev in charge',
    )
    
    hash_commit = fields.Char(
        string='Hash last commit',
    )

    pr_aproved_by = fields.Many2one(
        comodel_name='res.users',
        string='PR Approved by',
    )
    
    state = fields.Many2one(
        comodel_name='project.task.type',
        string='State',
        required=True,
    )
    
    project_id = fields.Many2one(
        comodel_name='project.project',
        string='Project',
        store=True,
    )

    personal_stage_type_ids = fields.Many2many(
        comodel_name='project.task.type',  # Modelo relacionado
        string='Personal Stage Types',  # Etiqueta en la interfaz de usuario
        compute='_compute_personal_stage_types',  # Método que calculará el valor
    )


    @api.onchange('task_id')
    @api.depends('task_id')
    def _compute_personal_stage_types(self):
        """
        Este método computa el valor del campo 'personal_stage_type_ids'
        basado en la lógica definida. Obtiene los 'stage_ids' relacionados
        con la tarea ('task_id').
        """
        for record in self:
            if record.task_id:
                record.project_id = record.task_id.project_id
                # record.personal_stage_type_ids = record.project_id.personal_stage_type_ids
                record.personal_stage_type_ids = record.project_id.type_ids
            else:
                record.personal_stage_type_ids = [(5, 0, 0)]


