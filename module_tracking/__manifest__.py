# module_tracking/__manifest__.py
{
    'name': 'Module Tracking',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Application to track modules',
    'description': """
        Este módulo ayuda a manejar las versiones de los repositorios que contiene el cliente
    """,
    'author': 'Your Name',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/tracking_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}