{
    'name': 'Git Tracking',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Application to track modules',
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