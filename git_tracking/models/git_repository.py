import os
import subprocess
from datetime import datetime

from odoo import models, _
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)

class GitRepository(models.Model):
    _name = 'git.repository'
    _description = 'Git Repository'


    def get_last_hash(self, path):
        _logger.error(str(f'git.get_last_hash(self, {path})'))
        try:
            result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise ValidationError(f"Error al obtener el último hash: {e}")


    def get_all_hashes(self, path):
        _logger.error(str(f'git.get_all_hashes(self, {path})'))
        
        try:
            result = subprocess.run(
                ["git", "log", "--pretty=format:%H"],
                cwd=path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.splitlines()
        except subprocess.CalledProcessError as e:
            raise ValidationError(f"Error al obtener todos los hashes: {e}")


    def get_name_commit_author(self, path):
        _logger.error(str(f'git.get_name_commit_author(self, {path})'))
        try:
            result = subprocess.run(
                ['git', 'log', '-1', '--format=%an'],
                cwd=path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()

        except subprocess.CalledProcessError as e:
            raise ValidationError(_(f"Error executing Git command: {e}"))
        except Exception as e:
            raise ValidationError(_(f"An unexpected error occurred: {e}"))


    def get_description(self, path, hash):
        _logger.error(str(f'git.get_description(self, {path}, {hash})'))
        try:
            result = subprocess.run(
                ["git", "show", "--quiet", "--pretty=format:%B", hash],
                cwd=path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise ValidationError(_(f"Error al obtener la descripción del commit: {e}"))


    def get_collaborator(self, path, hash):
        _logger.error(str(f'git.get_collaborator(self, {path}, {hash})'))
        try:
            result = subprocess.run(
                ["git", "show", "--quiet", "--pretty=format:%an", hash],
                cwd=path,
                capture_output=True,
                text=True,
                check=True
            )

            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise ValidationError(_(f"Error al obtener el nombre del colaborador: {e}"))


    def get_author_email(self, path):
        _logger.error(str(f'git.get_author_email(self, {path})'))
        try:
            result = subprocess.run(
                ['git', 'log', '-1', '--pretty=format:%ae'],
                cwd=path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise ValidationError(_(f"Error executing the command: {e} Standard output: {e.stdout} Error output: {e.stderr}"))
        except FileNotFoundError as e:
            raise ValidationError(f"Error: The directory '{path}' does not exist.")


    def get_commit_date(self, path):
        _logger.error(str(f'git.get_commit_date(self, {path})'))
        try:
            result = subprocess.run(
                ['git', 'log', '-1', '--pretty=format:%cd', '--date=iso'],
                cwd=path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise ValidationError(_(f"Error al ejecutar el comando: {e} Salida estándar: {e.stdout} Salida de error: {e.stderr}"))
        except FileNotFoundError as e:
            raise ValidationError(_(f"Error: El directorio '{path}' no existe."))


    def get_all_paths(self, path):
        _logger.error(str(f'git.get_all_paths(self, {path})'))
        try:
            result = subprocess.run(
                ["git", "submodule", "status", "--recursive"],
                cwd=path,
                capture_output=True,
                text=True,
                check=True
            )
            # Filtramos los paths de los submódulos del resultado
            lines = result.stdout.strip().splitlines()
            paths = [line.split()[1] for line in lines]
            return paths
        except subprocess.CalledProcessError as e:
            raise ValidationError(_(f"Error al obtener los paths de los submódulos: {e}"))


    def get_current_commit_date(self, path):
        _logger.error(str(f'git.get_current_commit_date(self, {path})'))
        try:
            hash_result = subprocess.run(
                ['git', 'rev-parse', 'HEAD'],
                cwd=path,
                capture_output=True,
                text=True,
                check=True
            )
            commit_hash = hash_result.stdout.strip()
            result = subprocess.run(
                ['git', 'show', '-s', '--format=%cd', '--date=iso', commit_hash],
                cwd=path,
                capture_output=True,
                text=True,
                check=True
            )
            commit_date_str = result.stdout.strip().split(' ')[0]
            return datetime.strptime(commit_date_str, '%Y-%m-%d')

        except subprocess.CalledProcessError as e:
            raise ValidationError(_(f"Error executing the command: {e} Standard output: {e.stdout} Error output: {e.stderr}"))
        except FileNotFoundError as e:
            raise ValidationError(_(f"Error: The directory '{path}' does not exist."))
        except ValidationError as e:
            raise ValidationError(_(f"Error formatting the date: {e}"))
        

    def get_remote_url(self, path):
        _logger.error(str(f'git.get_remote_url(self, {path})'))
        try:
            result = subprocess.run(
                ['git', '-C', path, 'remote', 'get-url', 'origin'],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise ValidationError(_(f"Error al obtener la URL remota: {e.stderr}"))


    def generate_commit_url(self, repo_url, commit_hash):
        _logger.error(str(f'git.generate_commit_url(self, {repo_url}, {commit_hash})'))

        _logger.error(repo_url)
        if repo_url.startswith('git@github.com:'):
            repo_url = repo_url.replace('git@github.com:', 'https://github.com/').replace('.git', '')
        elif repo_url.endswith('.git'):
            repo_url = repo_url.replace('.git', '')
        # if not repo_url.startswith('https://github.com/'):
        #     raise ValidationError("La URL proporcionada no es una URL de GitHub válida.")
        commit_url = f"{repo_url}/commit/{commit_hash}"
        return commit_url
    
    
    def validate_directory(self, directory_path):
        _logger.error(str(f'git.validate_directory(self, {directory_path})'))
        return os.path.isdir(directory_path)
    
    
    # def https_to_ssh(self, https_url):
    #     if not https_url.startswith('https://github.com/'):
    #         raise ValidationError(_("La URL proporcionada no es una URL HTTPS de GitHub."))
    #     ssh_url = https_url.replace('https://github.com/', 'git@github.com:').replace('.git', '')
    #     return ssh_url


    # def ssh_to_https(ssh_url):
    #     if not ssh_url.startswith('git@github.com:'):
    #         raise ValidationError(_("La URL proporcionada no es una URL SSH de GitHub."))
    #     https_url = ssh_url.replace('git@github.com:', 'https://github.com/').replace('.git', '')
    #     return https_url


    
