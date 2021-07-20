# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class stockpicking(models.Model):
    _inherit = 'stock.picking'

    purchase_ship_order = fields.Char(compute="_get_ship_order")

    @api.depends('purchase_id')
    def _get_ship_order(self):
        for record in self:
            if record.purchase_id.ship_order:
                record.purchase_ship_order = record.purchase_id.ship_order