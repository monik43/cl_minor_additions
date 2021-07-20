# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class stock_production_lot(models.Model):
    _inherit = 'stock.production.lot'
    CSN = fields.Char(string="CSN")