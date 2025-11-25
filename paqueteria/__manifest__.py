# -*- coding: utf-8 -*-
{
    'name': "Gestión de Paquetería y Camiones",

    'summary': "Modulo de paqueteria",

    'description': """
Modulo de ejemplo para una empresa de transportes:

- Gestion de paquetes
- Gestion de camiones
- Seguimiento de envios
- Control de conductores
    """,

    'author': "Javier Alcaraz",
    'website': "https://www.bembes.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Operations',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr'],

    # always loaded
    'data': [
        'security/paqueteria_security.xml',
        'security/ir.model.access.csv',

        'views/menu_views.xml',        
        'views/paquete_views.xml',
        'views/seguimiento_views.xml',
        'views/camion_views.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'application': True,
    'installable': True,
}

