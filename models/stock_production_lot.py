# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class stock_production_lot(models.Model):
    _inherit = 'stock.production.lot'

    CSN = fields.Char(string="CSN", compute="_get_CSN")

    def _get_CSN(self):
        for rec in self:
            if rec.env['stock.move.line'].search([('lot_id.id','=',rec.id)]):
                print(rec.env['stock.move.line'].search([('lot_id.id','=',rec.id)]))
                rec.CSN = rec.env['stock.move.line'].search([('lot_id.id','=',rec.id)])[0].CSN