# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class repair_line(models.Model):
    _inherit = 'mrp.repair.line'

    pieza_añadida = fields.Boolean('Pieza añadida?')

class mrp_repair(models.Model):
    _inherit = 'mrp.repair'
    po_rel = fields.Many2one(
        'purchase.order', string='Ticket relacionado', compute="_compute_po_rel")

    def _compute_po_rel(self):
        for rec in self:
            if rec.env['purchase.order'].search([('origin', '=', rec.name)]):
                rec.ticket_rel = rec.env['purchase.order'].search([('origin', '=', rec.name)])