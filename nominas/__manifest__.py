{
    'name': 'Nóminas de empleados SGE',
    'version': '1.0',
    'depends': ['base', 'hr'],
    'author': 'Javier Alcaraz Martín',
    'category': 'Human Resources',
    'data': [
        'security/ir.model.access.csv',
        'views/nomina_views.xml',
    ],
    'installable': True,
    'application': True,
}

