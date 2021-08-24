# -*- coding: utf-8 -*-

import time
from odoo import api, fields, models, _
from datetime import datetime
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError


class createclreparation_mrp(models.TransientModel):
    _name = 'create.clreparation_mrp'
    _description = "Crea un nuevo Test"

    origen_hdt = fields.Many2one(
        'helpdesk.ticket', 'Ticket reparación / Incidencia')
    tecnico_rep = fields.Many2one(
        'res.users', 'Técnico', domain="[('share','=',False)]", default=lambda self: self.env.user.id)
    origen_rep = fields.Many2one('mrp.repair', 'Reparación')
    date = fields.Datetime("Fecha", default=lambda self: fields.datetime.now())
    RMA = fields.Char('RMA')
    usr_credentials = fields.Many2one(
        'cl.user.credentials', 'Credenciales test usuario')
    reparation_test_basic = fields.One2many(
        'getmrp.data.basic', 'new_line_id_b', 'Test')
    reparation_test_user = fields.One2many(
        'getmrp.data.user', 'new_line_id_u', 'Test')
    product = fields.Many2one('product.product', 'Producto a reparar')

    def _test(self):
        print("test"*25)

    @api.multi
    def action_create_cl_reparation(self):
        self.ensure_one()
        res1 = self.env['cl.reparation'].browse(self._context.get('id',[]))
        res2 = self.env['cl.reparation.test.user'].browse(self._context.get('id',[]))
        res3 = self.env['cl.reparation.test.basic'].browse(self._context.get('id',[]))
        datamrp = self.env['mrp.repair'].browse(self._context.get('active_ids',[]))
        data_user = []
        data_basic = []
        for data in self.reparation_test_user:
            data_user.append([0,0,{'tname': data.tname, 'notes': data.notes, 'yes': data.yes, 'no': data.no}])

        for data in self.reparation_test_basic:
            data_basic.append([0,0,{'tname': data.tname, 'notes': data.notes, 'yes': data.yes, 'no': data.no}])
        print(data_user)
        res1.create({
            'usr_credentials': self.usr_credentials,
            'tecnico': self.tecnico_rep.id,
            'origen_rep': datamrp.id,
            'ticket': self.origen_hdt,
            'date': self.date,
            'RMA': self.RMA,
            #'reparation_test_user': data_user,
            #'reparation_test_basic': data_basic
            })
        return res1

    @api.multi
    def tprint(self):
        for line in self.reparation_test_basic:
            print(line.tname)
            print(line.notes)

    @api.model
    def default_get(self, fields):
        res = super(createclreparation_mrp, self).default_get(fields)
        data = self.env['mrp.repair'].browse(self._context.get('active_ids',[]))

        if data.product_id.id in (3412, 1279, 3405, 104, 1227, 242, 3379, 19, 400, 3165, 403, 3102, 3247, 1276, 3365, 3364, 3086, 297, 324, 330):
            print("/"*50)
            res.update({'reparation_test_basic': [(0, 0, {'tname': 'WIFI'}), (0, 0, {'tname': 'Teclado'}), (0, 0, {'tname': 'Touchpad'}), (0, 0, {'tname': 'Pantalla táctil (Si lo és)'}), (0, 0, {'tname': 'Prueba carga (cargador original)'}), (0, 0, {
                'tname': 'Prueba de carga (superior al 10%) 5% D 5% IZ'}), (0, 0, {'tname': 'Tornillos'}), (0, 0, {'tname': 'Embalaje'}), (0, 0, {'tname': 'Modo tablet (Táctil y que funcione KB y TP)'}), (0, 0, {'tname': 'Equipo de sustitución'})]})
        else:
            res.update({'reparation_test_basic': [(0, 0, {'tname': 'WIFI'}), (0, 0, {'tname': 'Teclado'}), (0, 0, {'tname': 'Touchpad'}), (0, 0, {'tname': 'Prueba carga (cargador original)'}), (0, 0, {
                'tname': 'Prueba de carga (superior al 10%) 5% D 5% IZ'}), (0, 0, {'tname': 'Tornillos'}), (0, 0, {'tname': 'Embalaje'}), (0, 0, {'tname': 'Equipo de sustitución'})]})

        res.update({'reparation_test_user': [(0, 0, {'tname': 'Battery Test'}), (0, 0, {'tname': 'Cámara #1 (1ª opción web: probar cámara)'}), (0, 0, {
                   'tname': 'Cámara #2'}), (0, 0, {'tname': 'Micrófono (1ª opción web: probar micrófono)'}), (0, 0, {'tname': 'Audio (videos YouTube etc)'})]})

        return res

class getmrpdata(models.TransientModel):
    _name = 'getmrp.data.user'
    _description = "Get MRP Repair user Data"

    new_line_id_u = fields.Many2one('create.clreparation_mrp')
        
    ureparation = fields.One2many('cl.reparation','reparation_test_user', 'Reparacion') 
    tname = fields.Char("Test                       ")
    notes = fields.Char("Observaciones")
    yes = fields.Boolean("Si")
    no = fields.Boolean("No")

class getmrpdata(models.TransientModel):
    _name = 'getmrp.data.basic'
    _description = "Get MRP Repair basic Data"

    new_line_id_b = fields.Many2one('create.clreparation_mrp')
        
    ureparation = fields.One2many('cl.reparation','reparation_test_user', 'Reparacion') 
    tname = fields.Char("Test                       ")
    notes = fields.Char("Observaciones")
    yes = fields.Boolean("Si")
    no = fields.Boolean("No")