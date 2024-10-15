{
    'name': 'Marea de código',
    'version': '17.0.0.1.0',
    'category': 'Tools',
    'summary': 'seguimiento de actualizaciones en clientes',
    'description': 'DevOps CI/CD',
    'author': 'Francisco Fiorentino',
    'depends': ['base', 'project'],
    'data': [
        'security/ir.model.access.csv',
        'views/devops_cicd.xml',
        # 'views/module_data_view.xml',
        # 'views/repository_path_view.xml',
        'views/partner_view.xml',
        'views/project_task_view.xml',

    ],
    'images': [
        'static/description/icon.png',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}                                                                                                                                                                                                                            