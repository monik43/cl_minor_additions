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
    reparation_test_basic = fields.One2many('cl.reparation.newtest','brep', 'Test básico')
    reparation_test_user = fields.One2many('cl.reparation.newtest','urep', 'Test usuario')
    test_pasado = fields.Boolean(compute="_get_test_pasado")

    def _get_test_pasado(self):
        for rec in self:
            pasado = True
            for testline in rec.reparation_test_basic:
                if testline.no == True or testline.yes != True:
                    pasado = False
                    break

            if rec.usr_credentials:
                for testline in rec.reparation_test_user:
                    if testline.no == True or testline.yes != True:
                        pasado = False
                        break
                    
            rec.test_pasado = pasado


class reparation_test(models.Model):
    _name = 'cl.reparation.newtest'
    origin = fields.Char()
    urep = fields.Many2one('cl.reparation','reparation_test_user')
    brep = fields.Many2one('cl.reparation','reparation_test_basic')
    name = fields.Char("Test                       ", readonly="True")
    notes = fields.Char("Observaciones")
    yes = fields.Boolean("Si")
    no = fields.Boolean("No")