# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class purchase_order(models.Model):
    _inherit = 'purchase.order'

    @api.onchange('order_line')
    def update_order_lines_fields(self):
        for rec in self:
            for partner in rec.order_line.product_id.seller_ids.name:
                print(partner)
                """for line in rec.order_line:
                        print(line.product_id.seller_ids.name)"""
