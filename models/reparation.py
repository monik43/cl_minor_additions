# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import datetime

class reparation(models.Model):
    _name = 'cl.reparation'
    _description = 'Test de la reparación'

    
    tecnico = fields.Many2one('res.partner', domain="[('share','=',False)]")
    origen_rep = fields.Many2one('mrp.repair')
    ticket = fields.Many2one('helpdesk.ticket')
    #date = fields.Date(string="Date" ,default=datetime.now())

    RMA = fields.Char()

    reparation_test = fields.One2many('cl.reparation.test','reparation')


class reparation_test(models.Model):
    _name = 'cl.reparation.test'

    reparation = fields.One2many('cl.reparation','reparation_test') 
    it_works = fields.Boolean(string="Si")
    doesnot_work = fields.Boolean(string="No")
    notes = fields.Text()

