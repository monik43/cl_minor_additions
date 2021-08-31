# -*- coding: utf-8 -*-
{
    'name': "cl_minor_additions",

    'summary': """
        Adiciones menores a Odoo""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Cloudalia Educacion",
    'website': "https://cloudaliaeducacion.com/",
    'category': 'Uncategorized',
    'version': '11.0.0.6',
    'depends': ['base', 'stock', 'cloudedu_mods', 'account', 'filtro_comercial-main', 'helpdesk', 'mrp_repair'],
    'data': [
        'views/helpdesk_views.xml',

        'views/reparation_views.xml',

        'data/user_credentials.xml',
        'views/mrp_repair_views.xml',
        'views/stock_views.xml',
        'views/mail_views.xml',
        'views/purchase_order_mrp_wiz.xml',
        'views/account_invoice_views.xml',
        'views/account_templates.xml',
        'views/web_assets.xml',
        'views/report_picking_final_2.xml',
        'wizard/create_reparation.xml',
    ],
    'qweb': [
        'static/src/xml/account_payment.xml',
    ],
}
