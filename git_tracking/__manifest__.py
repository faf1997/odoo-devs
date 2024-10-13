{
    'name': 'Git Tracking',
    'version': '17.0.0.1.0',
    'category': 'Tools',
    'summary': 
'''Application to track modules. 
In order to analyze the repository from the application, you must run the following command in the terminal to give odoo permissions:
chown -R odoo:odoo /repository_path
''',
    'description': """
        Este módulo ayuda a manejar las versiones de los repositorios que contiene el cliente
    """,
    'author': 'Francisco Fiorentino',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'data/action_server.xml',
        'views/module_data_view.xml',
        'views/repository_path_view.xml',

    ],
    'images': [
        'static/description/icon.png',
        'static/description/icon.svg'
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}