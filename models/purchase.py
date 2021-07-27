# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class purchase_order(models.Model):
    _inherit = 'purchase.order'

    @api.multi
    def print_fields(self):
        for rec in self:
            fields = rec.fields_get()
            for field in fields:
                for val in field:
                    print(field, " ", val)


    @api.onchange('order_line')
    def update_order_lines_fields(self):
        for rec in self:
            for line in rec.order_line:
                for seller_id in line.product_id.seller_ids:
                    if rec.partner_id == seller_id.name:
                        line.price_unit = seller_id.price
