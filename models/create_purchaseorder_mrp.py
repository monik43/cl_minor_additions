# -*- coding: utf-8 -*-
import time
from odoo import api, fields, models, _
from datetime import datetime
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError


class createpurchaseordermrp(models.TransientModel):
    _inherit = 'create.purchaseorder_mrp'

    @api.multi
    def action_create_purchase_order_mrp_fix(self):
        self.ensure_one()
        res = self.env['purchase.order'].browse(self._context.get('id', []))
        value = []
        partner_pricelist = self.partner_id.property_product_pricelist
        mrp_repair_name = ""
        for data in self.new_order_line_ids:
            final_price = 00.0
            mrp_repair_name = data.order_id.name
            print(mrp_repair_name)
            if partner_pricelist:
                product_context = dict(
                    self.env.context, partner_id=self.partner_id.id, date=self.date_order, uom=data.product_uom.id)
                final_price, rule_id = partner_pricelist.with_context(product_context).get_product_price_rule(
                    data.product_id, data.product_qty or 1.0, self.partner_id)
            else:
                final_price = data.product_id.standard_price

            value.append([0, 0, {
                'product_id': data.product_id.id,
                'name': data.name,
                'product_qty': data.product_qty,
                'order_id': data.order_id.id,
                'product_uom': data.product_uom.id,
                'taxes_id': ([(6, 0, data.product_id.supplier_taxes_id.ids)]),
                'date_planned': datetime.today(),
                'price_unit': final_price,
            }])

        res.create({
            'partner_id': self.partner_id.id,
            'date_order': self.date_order,
            'order_line': value,
            'origin': mrp_repair_name,
            'partner_ref': mrp_repair_name,
            'picking_type_id': self.warehouse.id,
        })

        return res

    
