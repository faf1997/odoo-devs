from odoo import models, fields, api, _
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

    url_remote = fields.Char(
        string='URL remote',
        readonly=True
    )


    @api.model
    def create_module_data(self, name, email, path_submodule, hash, date, commit_description, is_submodule, url_remote):
        data_module = self.env['module.data'].create({
            'name': name,
            'email': email,
            'path_submodules': path_submodule,
            'hash': hash,
            'date': date,
            'commit_description': commit_description,
            'is_submodule': is_submodule,
            'url_remote': url_remote,
        })
        _logger.error(str(data_module))
        return data_module.id


    def calculate_submodule_paths(self, absolute_path, submodule_path_list):
        submodule_paths = []
        for path in submodule_path_list:
            submodule_paths.append(f'{absolute_path}/{path}')
        return submodule_paths


    def calculate_submodules(self, principal_path, git):
        submodules_paths = self.calculate_submodule_paths(
            principal_path, 
            git.get_all_paths(principal_path)
            )
        
        submodule_ids = []
        for submodules_path in submodules_paths:
            _logger.error(str(submodules_path))
            
            hash = git.get_last_hash(submodules_path)
            if not self.search_count([('hash', '=', hash)]) > 0:
                submodule_ids.append(
                    self.create_module_data(
                        git.get_name_commit_author(submodules_path),
                        git.get_author_email(submodules_path),
                        submodules_path.split(principal_path)[1],
                        hash,
                        git.get_current_commit_date(submodules_path),
                        git.get_description(submodules_path, hash),
                        True,
                        git.generate_commit_url(git.get_remote_url(submodules_path), hash)
                        # git.get_remote_url(submodules_path)
                    )
                )
        return submodule_ids


    def action_check_changes(self):
        # self.ensure_one()
        recs = self.env['repository.path'].search([('active', '=', True)], limit=1)
        if len(recs) == 0:
            raise ValidationError(_('check that the repository path is configured or correct'))

        path = recs[0].name
        git = self.env['git.repository']
        for rec in self:
            hash = git.get_last_hash(path)
            if not self.search_count([('hash', '=', hash)]) > 0:
                rec.hash = hash
                rec.name = git.get_name_commit_author(path)
                rec.email = git.get_author_email(path)
                rec.commit_description = git.get_description(path, rec.hash)
                rec.path_submodules = path
                rec.date = git.get_current_commit_date(path)
                rec.url_remote = git.generate_commit_url(git.get_remote_url(path), hash)
                rec.submodules = self.calculate_submodules(path, git)
            else:
                rec.unlink()



