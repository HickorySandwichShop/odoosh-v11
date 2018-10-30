# -*- coding: utf-8 -*-

{
    'name': 'BOM Extension',
    'version': '1.0',
    'category': 'Manufacturing',
    'summary': "Manufacturing",
    'description': """
       """,
    'author': 'Confianz Global',
    'website': 'http://confianzit.com',
    'images': [],

    'data': [
             'wizard/update_bom_wizard.xml',
             'views/product_template.xml',
            ],

    'depends': ['mrp'],
    'installable': True,
    'auto_install': False,
    'application': False,
}


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
