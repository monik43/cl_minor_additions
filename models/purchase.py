# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class purchase_order(models.Model):
    _inherit = 'purchase.order'

    @api.onchange('order_line')
    def update_order_lines_fields(self):
        for rec in self:
            for line in rec.order_line:
                if rec.partner_id in line.seller_ids:
                    print(line.seller_ids)