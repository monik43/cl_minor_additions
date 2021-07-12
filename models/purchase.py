# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class purchase_order(models.Model):
    _inherit = 'purchase.order'

    @api.onchange('order_line')
    def update_order_lines_fields(self):
        for record in self:
            for line in self.order_line:
                if line.price_unit != line.product_id.lst_price:
                    line.price_unit = line.product_id.lst_price
