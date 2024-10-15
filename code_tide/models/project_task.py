from odoo import models, fields, api, tools, _
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)


class ProjectTask(models.Model):
    _inherit = 'project.task'



    def action_create_cicd(self):
        self.ensure_one()
        devops_cicd = self.env['devops.cicd']
        for task in self:
            if task.partner_id.company_type != 'company':
                raise ValidationError(_('Only companies can create CI/CD tasks'))

            is_create = self.env['devops.cicd'].search([('task_id', '=', task.id)], limit=1)
            if not is_create:
                devops_cicd.create({
                    'task_id': task.id,
                    'customer_id': task.partner_id.id,
                    'date_start': fields.Date.today(),
                    'state': task.stage_id.id,
                    # 'personal_stage_type_ids': [(6, 0, task.stage_id.project_stage_type_ids.ids)], 
                })