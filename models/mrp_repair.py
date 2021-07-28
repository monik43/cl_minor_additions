# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.osv import orm
from lxml import etree


class repair_line(models.Model):
    _inherit = 'mrp.repair.line'

    pieza_añadida = fields.Boolean('Pieza añadida?')

    @api.onchange('type', 'repair_id')
    def onchange_operation_type(self):
        """ On change of operation type it sets source location, destination location
        and to invoice field.
        @param product: Changed operation type.
        @param guarantee_limit: Guarantee limit of current record.
        @return: Dictionary of values.
        """
        if not self.type:
            self.location_id = False
            self.location_dest_id = False
        elif self.type == 'add':
            self.onchange_product_id()
            args = self.repair_id.company_id and [('company_id', '=', self.repair_id.company_id.id)] or []
            warehouse = self.env['stock.warehouse'].search(args, limit=1)
            self.location_id = self.repair_id.location_id
            self.location_dest_id = self.env['stock.location'].search([('usage', '=', 'production')], limit=1).id
        else:
            self.price_unit = 0.0
            self.tax_id = False
            self.location_id = self.env['stock.location'].search([('usage', '=', 'production')], limit=1).id
            self.location_dest_id = self.env['stock.location'].search([('scrap_location', '=', True)], limit=1).id

class mrp_repair(models.Model):
    _inherit = 'mrp.repair'

    n_lot_id = fields.Many2one(
        'stock.production.lot', 'Lote/Nº de serie',
        domain="[('product_id','=', product_id)]",
        help="Los productos reparados pertenecen todos a este lote")

    po_rel = fields.Many2one(
        'purchase.order', string='Purchase relacionada', compute="_compute_po_rel")

    rep_conf = fields.Boolean(default=False,compute="_get_state")

    def _compute_po_rel(self):
        for rec in self:
            if rec.env['purchase.order'].search([('partner_ref','like',rec.name)]) != False:
                rec.po_rel = rec.env['purchase.order'].search([('partner_ref','=',rec.name)])
            
    def _get_state(self):
        for rec in self:
            if rec.state == 'confirmed':# and rec.rep_conf != True:
                print("helloworld!")
