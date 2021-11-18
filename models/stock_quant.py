# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class stock_quant(models.Model):
    _inherit = "stock.quant"

    CSN = fields.Char("CSN", compute="_compute_CSN")

    def _compute_CSN(self):
        for rec in self:
            if rec.lot_id and rec.lot_id.CSN:
                rec.CSN = rec.lot_id.CSN