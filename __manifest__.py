# -*- coding: utf-8 -*-
{
    'name': "Cloudalia Module Misc",

    'summary': """
        Adiciones menores a Odoo""",

    'description': """
        Cambios en los modelos:
        - create_purchaseorder_mrp
        - helpdesk
        - mail_activity
        - mrp_repair
        - purchase
        - stock_move
        - stock_picking
        - stock_production_lot

        Nuevos modelos:
        - cl.reparation
        - cl.user.credentials

        Wizard:
        - cl.create.reparation
    """,

    'author': "Cloudalia Educacion",
    'website': "https://cloudaliaeducacion.com/",
    'category': 'Uncategorized',
    'version': '11.0.0.10',
    'depends': ['base', 'stock', 'mrp_repair', 'helpdesk', 'account', 'cloudedu_mods', 'filtro_comercial-main'],
    'data': [
        'views/web_assets.xml',
        'views/account_invoice_views.xml',
        'views/account_templates.xml',
        'views/report_picking_final_2.xml',
        'data/user_credentials.xml',
        'views/purchase_order_mrp_wiz.xml',
        'views/mrp_repair_views.xml',
        'views/mail_views.xml',
        'views/helpdesk_views.xml',
        'views/stock_views.xml',
        'views/reparation_views.xml',
        'wizard/create_reparation.xml',
    ],
    'qweb': [
        'static/src/xml/account_payment.xml',
    ],
}
