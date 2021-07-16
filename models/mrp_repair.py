# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class repair_line(models.Model):
    _inherit = 'mrp.repair.line'

    pieza_añadida = fields.Boolean('Pieza añadida?')

    purchase_order_exists = fields.Boolean(
        'Existe purchase order?', compute="_compute_purchase_order_exists")
    po_rel = fields.Many2one(
        'purchase.order', string='Ticket relacionado', compute="_compute_po_rel")

    def _compute_po_rel(self):
        for rec in self:
            if rec.env['purchase.order'].hd_ticket.search([('origin', '=', rec.name)]):
                rec.ticket_rel = rec.env['purchase.order'].hd_ticket.search([('origin', '=', rec.name)])