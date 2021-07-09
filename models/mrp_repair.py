# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class repair_line(models.Model):
    _inherit = 'mrp.repair.line'

    pieza_añadida = fields.Boolean('Pieza añadida?')