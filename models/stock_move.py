# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class stockmove(models.Model):
    _inherit = 'stock.move'

    ship_order_move = fields.Char(compute="_get_purchase_ship_order")

    @api.depends('picking_id')
    def _get_purchase_ship_order(self):

        for record in self:
            stock_picking = record.env['stock.picking']
            if stock_picking.browse(record.picking_id.id):
                record.ship_order_move = stock_picking.browse(
                    record.picking_id.id).purchase_ship_order


class stockmoveline(models.Model):
    _inherit = 'stock.move.line'

    ship_order_move = fields.Char(compute="_get_purchase_ship_order")
    CSN = fields.Many2one('stock.production.csn', 'CSN')

    def _get_purchase_ship_order(self):
        for record in self:
            if record.env['stock.picking'].browse(record.picking_id.id):
                record.ship_order_move = record.env['stock.picking'].browse(
                    record.picking_id.id).purchase_ship_order
