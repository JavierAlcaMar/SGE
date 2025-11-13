# -*- coding: utf-8 -*-
{
    'name': "Gestion de Ordenadores",

    'summary': "Registro de ordenadores, componentes y usuarios",

    'description': """
Long description of module's purpose
    """,

    'author': "Javier Alcaraz Martin",
    'website': "https://www.bembes.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'IT',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/pc_management_security.xml',
        'security/ir.model.access.csv',
        'views/ordenador_views.xml',
        'views/componente_views.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'installable': True,
    'application': True,
}

