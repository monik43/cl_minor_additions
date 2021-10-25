# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class purchase_order(models.Model):
    _inherit = 'purchase.order'

    @api.onchange('order_line')
    def update_order_lines_fields(self):
        for rec in self:
            for line in rec.order_line:
                for seller_id in line.product_id.seller_ids:
                    if rec.partner_id == seller_id.name:
                        line.price_unit = seller_id.price
    
    @api.multi
    def open_purchase(self):
        for rec in self:
            url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
            rec_url = (
                url + "/web#id=" + str(self.id) + "&view_type=form&model=purchase.order"
            )
            client_action = {
                "type": "ir.actions.act_url",
                "name": self.display_name,
                "target": "new",
                "url": rec_url,
            }

            return client_action
