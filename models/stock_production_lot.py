# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class stock_production_lot(models.Model):
    _inherit = 'stock.production.lot'
    
    CSN = fields.Many2one('stock.production.csn','CSN')

class stock_production_csn(models.Model):
    _name = 'stock.production.csn'
    _description = "CSN of stock.production.lot"

    CSN = fields.Char()