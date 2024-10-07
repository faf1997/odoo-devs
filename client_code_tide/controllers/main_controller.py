import re
import subprocess
from odoo import http
from odoo.http import request

import logging




_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)



def get_odoo_major_version(version_str):
    match = re.search(r'\b\d+\.\d+\b', version_str)
    return match.group() if match else None


def get_odoo_version():
    try:
        # Intenta ejecutar el comando 'odoo --version'
        result = subprocess.run(['odoo-bin', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"Error: {result.stderr.strip()}"
    except FileNotFoundError:
        try:
            # Si 'odoo' no se encuentra, intenta con 'odoo-bin --version'
            result = subprocess.run(['odoo', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return f"Error: {result.stderr.strip()}"
        except FileNotFoundError:
            return "Error: Neither 'odoo' nor 'odoo-bin' command found"
    except Exception as e:
        return f"Unexpected error: {str(e)}"



class ModuleController(http.Controller):
    
    @http.route('/installed_modules', type='json', auth='public')
    def get_installed_modules(self):
        installed_modules = request.env['ir.module.module'].sudo().search([('state', '=', 'installed'), ('author', '!=', 'Odoo S.A.')])
        modules_info = [{'name': module.name, 'version': module.latest_version or 'N/A'} for module in installed_modules]
        odoo_version = get_odoo_major_version(get_odoo_version())
        return {'installed_modules': [modules_info], 'odoo_version': odoo_version}


    
    

        
        
