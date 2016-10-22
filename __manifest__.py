# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Alipay Payment Services',
    'version': '1.0',
    'category': 'Point of Sale',
    'sequence': 6,
    'summary': 'Alipay support for Point Of Sale',
    'description': """
Allow alipay POS payments
==============================

This module allows customers to pay for their orders with credit
cards. The transactions are processed by alipay (developed by Wells
Fargo Bank). A alipay merchant account is necessary. It allows the
following:

* Fast payment by alipay while on the payment screen
* Combining of cash payments and credit card payments
* Cashback
* Supported:
    """,
    'depends': ['web', 'barcodes', 'point_of_sale'],
    'website': '',
    'data': [
        'data/pos_alipay_data.xml',
        'security/ir.model.access.csv',
        'views/pos_alipay_templates.xml',
        'views/pos_alipay_views.xml',
        'views/pos_alipay_transaction_templates.xml',
    ],
    'demo': [
        'data/pos_alipay_demo.xml',
    ],
    'qweb': [
        'static/src/xml/pos_alipay.xml',
    ],
    'installable': True,
    'auto_install': False,
}
