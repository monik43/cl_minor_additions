# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import datetime

class reparation(models.Model):
    _name = 'cl.reparation'
    _description = 'Test de la reparación'

    usr_credentials = fields.Many2one('cl.user.credentials')
    tecnico = fields.Many2one('res.users','Técnico', domain="[('share','=',False)]")
    origen_rep = fields.Many2one('mrp.repair', 'Reparación')
    ticket = fields.Many2one('helpdesk.ticket')
    date = fields.Datetime("Fecha")
    RMA = fields.Char('RMA')
    reparation_test_user = fields.One2many('cl.reparation.test','ureparation', 'Test usuario')
    reparation_test_basic = fields.One2many('cl.reparation.test','breparation', 'Test usuario')
    test_pasado = fields.Boolean()


class reparation_test(models.Model):
    _name = 'cl.reparation.test'

    ureparation = fields.One2many('cl.reparation','reparation_test', 'Reparacion')
    breparation = fields.One2many('cl.reparation','reparation_test', 'Reparacion')
    name = fields.Char("Test                       ", readonly="True")
    notes = fields.Char("Observaciones")
    yes = fields.Boolean("Si")
    no = fields.Boolean("No")