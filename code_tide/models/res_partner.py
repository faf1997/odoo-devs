import re
from odoo import fields, models, api
from odoo.exceptions import ValidationError



def is_github_ssh_link(url):
    pattern = r'^git@github\.com:.*\.git$'
    return bool(re.match(pattern, url))

def is_github_repo_link(url):
    pattern = r'^https:\/\/github\.com\/[^\/]+\/[^\/]+(?:\.git)?$'
    return bool(re.match(pattern, url))


class ResPartner(models.Model):
    _inherit = 'res.partner'


    # git_repository = fields.Char(compute='_validate_repository', string='Repositorio ssh')
    git_repository = fields.Char(string='Repositorio ssh')


    @api.onchange('git_repository')
    def _validate_repository(self):
        for partner in self:
            if partner.git_repository:
                is_github_ssh = is_github_ssh_link(partner.git_repository)
                is_github_link = is_github_repo_link(partner.git_repository)
                if not is_github_ssh and not is_github_link:
                    partner.git_repository = False
                elif is_github_link:
                    partner.git_repository = partner.git_repository.replace( 'https://github.com/', 'git@github.com:')
