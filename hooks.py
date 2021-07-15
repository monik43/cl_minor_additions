# -*- coding: utf-8 -*-
from odoo import api, SUPERUSER_ID

def pre_init_hook(cr):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env.['mail.activity.type'].create({'name': 'Respuesta'})