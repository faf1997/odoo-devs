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

    url_remote = fields.Char(
        string='URL remote',
        readonly=True
    )


    def get_last_two_records(self):
        last_two_records = self.search(['is_submodule', '=', False], order='id desc', limit=2)
        return last_two_records


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


    def calculate_submodule_paths(self, absolute_path, submodule_path_list, git):
        submodule_paths = []
        for path in submodule_path_list:
            full_path = f'{absolute_path}/{path}'
            if git.validate_directory(full_path): # descarto los directorios que se hayan manipulado sin git
                submodule_paths.append(full_path)
        return submodule_paths


    def calculate_submodules(self, principal_path, git):
        submodules_paths = self.calculate_submodule_paths(
            principal_path,
            git.get_all_paths(principal_path),
            git
        )

        submodule_ids = []
        for submodules_path in submodules_paths:
            _logger.error(str(submodules_path))
            if not git.validate_directory(submodules_path):
                continue
            hash = git.get_last_hash(submodules_path)
            hash_id = self.search([('hash', '=', hash)])
            
            if not hash_id:
                
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
                    )
                )
            else:
                # raise ValidationError(str(hash_id))
                submodule_ids.append(hash_id.id)
        return submodule_ids


    def action_check_changes(self):
        self.ensure_one()
        _logger.error('ModuleData.action_check_changes()')
        recs = self.env['repository.path'].sudo().search([('active', '=', True)], limit=1)
        _logger.error(f'{recs}')

        if len(recs) == 0:
            raise ValidationError(_('check that the repository path is configured or correct'))

        path = recs[0].name
        git = self.env['git.repository']
        hash = git.get_last_hash(path)
        _logger.error(f'{hash}')
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
                rec.unlink(active=True)


    def update_cron_data(self):
        recs = self.env['repository.path'].sudo().search([('active', '=', True)], limit=1)
        if len(recs) == 0:
            raise ValidationError(_('check that the repository path is configured or correct'))

        vals_list = [{
            'name': '',
            'email': '',
            'path_submodules': '',
            'hash': '',
            'commit_description': '',
            'url_remote': '',
        }]
        self.create(vals_list)

        path = recs[0].name
        git = self.env['git.repository']

        module_data = self.env['module.data'].sudo().search(
            [
            ('name', '=', ''),
            ('email', '=', ''),
            ('path_submodules', '=', ''),
            ('hash', '=', ''),
            ('commit_description', '=', ''),
            ('url_remote', '=', '')
            ],
            limit=1
        )

        for rec in module_data:
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
                rec.unlink_aux()
        residual = self.env['module.data'].sudo().search([('name', '=', False)], limit=0)
        _logger.error(f'{residual}')
        
        for rec in residual:
            rec.unlink(active=True)


    def unlink(self, active=False):
        if not active:
            raise ValidationError('No está permitido eliminar registros')
        else:
            super(ModuleData, self).unlink()
