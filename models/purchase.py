# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class purchase_order(models.Model):
    _inherit = 'purchase.order'

    pid = fields.Char(compute="_get_pid")

    def _get_pid(self):
        for rec in self:
            rec.pid = rec.origin[4:]
            print(rec.pid)

    @api.onchange('order_line')
    def update_order_lines_fields(self):
        for rec in self:
            for line in rec.order_line:
                for seller_id in line.product_id.seller_ids:
                    if rec.partner_id == seller_id.name:
                        line.price_unit = seller_id.price
