# -*- coding: utf-8 -*-
import time
from odoo import api, fields, models, _
from datetime import datetime
import odoo.addons.decimal_precision as dp


class createpurchaseordermrp(models.TransientModel):
    _inherit = 'create.purchaseorder_mrp'

    @api.depends('new_order_line_ids')
    def _compute_warehouse_and_partner_id(self):
        ASUS_ID = 12300
        HP_ID = 10198
        war_dict = {
            'asus_iw': 0,
            'asus_oow': 0,
            'hp_iw': 0,
            'hp_oow': 0,
        }

        def check_wp(c_id, c_w, dict):
            if c_id == ASUS_ID:
                if c_w == 'iw':
                    dict['asus_iw'] += 1
                elif c_w == 'oow':
                    dict['asus_oow'] += 1
            elif c_id == HP_ID:
                if c_w == 'iw':
                    dict['hp_iw'] += 1
                elif c_w == 'oow':
                    dict['hp_oow'] += 1
        
        def bigger(dict):
            asus_iw = dict['asus_iw']
            asus_oow = dict['asus_oow']
            hp_iw = dict['hp_iw']
            hp_oow = dict['hp_oow']
            if asus_iw >= asus_oow and asus_iw >= hp_iw and asus_iw >= hp_oow:
                wh_id = 20
                p_id = ASUS_ID
            elif hp_iw >= asus_iw and hp_iw >= asus_oow and hp_iw >= hp_oow:
                wh_id = 26
                p_id = HP_ID
            elif asus_oow >= asus_iw and asus_oow >= hp_iw and asus_oow >= hp_oow:
                wh_id = 32
                p_id = ASUS_ID
            elif hp_oow >= asus_iw and hp_oow >= asus_oow and hp_oow >= hp_iw:
                wh_id = 32
                p_id = HP_ID

            return wh_id, p_id

        for rec in self:
            for line in rec.new_order_line_ids:
                check_wp(line.seller_id.id, line.warranty, war_dict)

            wh_id, p_id = bigger(war_dict)
            rec.warehouse = self.env['stock.picking.type'].browse(wh_id)
            rec.partner_id = self.env['res.partner'].browse(p_id)
            
    warehouse = fields.Many2one('stock.picking.type', string='Recepción',readonly=False, required=True, compute="_compute_warehouse_and_partner_id")
    partner_id = fields.Many2one("res.partner", string="Vendor", readonly=False, required=True, compute="_compute_warehouse_and_partner_id")

    @api.onchange("new_order_line_ids")
    def _onchange_new_order_line_ids(self):
        res = {}
        s_ids = []
        self.ensure_one()
        for p in self.new_order_line_ids:
            for s in p.product_id.seller_ids:
                if s.name.id not in s_ids:
                    s_ids.append(str(s.name.id))
        res['domain'] = {'partner_id': [('id', 'in', s_ids)]}
        return res

    @api.model
    def default_get(self,  default_fields):
        res = super(createpurchaseordermrp, self).default_get(default_fields)
        data = self.env['mrp.repair'].browse(
            self._context.get('active_ids', []))
        update = []
        for record in data.operations:
            if record.product_id.default_code != "COMPENSACION":
                seller_id = None
                for line in record.product_id.seller_ids:
                    if line.name.id in (12300,10198):
                        seller_id = line.name.id

                update.append((0, 0, {
                    'product_id': record.product_id.id,
                    'product_uom': record.product_uom.id,
                    'order_id': record.repair_id.id,
                    'name': record.name,
                    'product_qty': record.product_uom_qty,
                    'price_unit': record.price_unit,
                    'product_subtotal': record.price_subtotal,
                    "warranty": record.warranty,
                    "seller_id": seller_id,
                }))
        res.update({'new_order_line_ids': update})
        return res

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

class getsale_mrpdata(models.TransientModel):
    _inherit = "getsale.mrpdata"

    seller_ids = fields.Many2one('res.partner', required=True, readonly=False)
    seller_id = fields.Many2one('res.partner', required=True, readonly=False)