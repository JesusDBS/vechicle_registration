# -*- coding: utf-8 -*-
{
    'name': "vehicle_register",

    'summary': """Module to register vehicles""",

    'description': """Module to register vehicles""",

    'author': "Jesús David Briceño Salazar",

    'category': 'Registro Vehicular',
    'version': '0.1',

    'depends': ['contacts'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/data.xml',
        'views/res_partner.xml',
        'views/menu.xml',
        'views/vehicle.xml',
        'views/driver_license.xml',
        'views/vehicle_type.xml',
        'views/vehicle_brand.xml',
        'views/driver_license_type.xml',
        'views/logs.xml',
    ],
    
    "images": ['static/description/icon.png'],
}
