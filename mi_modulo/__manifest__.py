# -*- coding: utf-8 -*-
{
    'name': "mi_modulo",

    'summary': "Mi primer modulo",

    'description': """
Creando mi primer modulo para la asignatura de SGE
    """,

    'author': "Javier Alcaraz",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'SGE/Mi Modulo',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
	'security/security.xml',
        'security/ir.model.access.csv',
        'views/ejemplo_views.xml',
	'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'installable': True,
    'application': True,
    'license': 'LGPL-3'
}

