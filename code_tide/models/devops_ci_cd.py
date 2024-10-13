from odoo import models, fields

class DevOpsCiCd(models.Model):
    _name = 'devops.cicd'
    _description = 'Continuous Integration / Continuous Deployment'

    # name = fields.Char(string='Name', required=True)
    # description = fields.Text(string='Description')
    
    github_status = fields.Selection([#deberá actualizarse automaticamente
        ('updated', 'Actualizado'),#cero módulos desactualizados
        ('outdated', 'Desactualizado'),#1-2 módulos desactualizados
        ('critical', 'Crítico'),# más de 2 módulos desactualizados
    ],
    string='Github status',
    help='\nActualizado: cero módulos desactualizados\nDesactualizado: uno a 2 módulos desactualizados\nCrítico: más de 2 módulos desactualizados'
    )
    
    