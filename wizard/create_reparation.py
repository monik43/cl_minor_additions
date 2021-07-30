# -*- coding: utf-8 -*-

import time
from odoo import api, fields, models, _
from datetime import datetime
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError


class createclreparation_mrp(models.TransientModel):
    _name = 'create.clreparation_mrp'
    _description = "Crea un nuevo Test"

    tecnico_rep = fields.Many2one(
        'res.users', 'Técnico', domain="[('share','=',False)]", default=lambda self: self.env.user.id)
    origen_rep = fields.Many2one('mrp.repair', 'Reparación')
    date = fields.Datetime("Fecha", default=lambda self: fields.datetime.now())
    RMA = fields.Char('RMA')
    usr_credentials = fields.Many2one(
        'cl.user.credentials', 'Credenciales test usuario')
    reparation_test_basic = fields.One2many(
        'cl.reparation.test', 'reparation', 'Test')
    reparation_test_user = fields.One2many(
        'cl.reparation.test', 'reparation', 'Test')

    @api.model
    def default_get(self, fields):
        res = super(createclreparation_mrp, self).default_get(fields)
        res.update({'reparation_test_basic': [(0, 0, {'tname':'WIFI'})]})
        return res
