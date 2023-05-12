# -*- coding: utf-8 -*-

{
    'name': 'AGR - Warehouse Management',
    'version': '1.2',
    'author': "Ing. José Andrés Hernández Bustio, . Enrique ..., Ing. Orlando Martinez Bao (YYOGestiono)",
    'license': 'LGPL-3',
    'summary': 'Inventory, Logistic, Storage',
    'description': """
Customizing stock odoo module
==================================================

Customization description:
**************************
* Customizing stockpicking report
    """,
    'depends': ['stock', 'product_arancel', 'stock_account', 'stock_picking_reception_report'],
    'category': 'Warehouse Management',
    'data': [
        'views/res_company.xml',
        'views/res_partner.xml',
        # 'views/stock_picking_view.xml',
        'views/stock_warehouse_views.xml',
        'views/product_view.xml',
        'views/stock_inventory_valuation_view.xml',
        'security/ir.model.access.csv',
        # 'views/stock_reception_report_view.xml',
        'report/report_stock_inventory_valuation_template.xml',
        'report/report_stock_inventory_valuation.xml',
        'report/report_stock_inventory_valuation_layout.xml',
        
    ],
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: