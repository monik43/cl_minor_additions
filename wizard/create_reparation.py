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
        """self.ensure_one()
        res = self.env['cl.reparation'].browse(self._context.get('id', []))"""
        basic_data, user_data = []

        for data in self.reparation_test_basic:
            basic_data.append([0, 0, {'breparation': data.breparation, 'tname': data.tname,
                              'notes': data.notes, 'yes': data.yes, 'no': data.no}])

        for data in self.reparation_test_user:
            user_data.append([0, 0, {'ureparation': data.ureparation, 'tname': data.tname,
                             'notes': data.notes, 'yes': data.yes, 'no': data.no}])

        print(basic_data)
        print(user_data)
        """res.create({
            'usr_credentials': self.usr_credentials, 
            'tecnico': self.tecnico_rep, 
            'origen_rep': self.origen_rep,
            'ticket': self.origen_hdt, 
            'date': self.date, 
            'RMA': self.RMA, 
            'reparation_test_basic': basic_data, 
            'reparation_test_user': user_data
            })

        print("/"*25,res)
        return res"""

    @api.multi
    def tprint(self):
        print("test"*25)

    @api.model
    def default_get(self, fields):
        res = super(createclreparation_mrp, self).default_get(fields)
        data = self.env['mrp.repair'].browse(self._context.get('active_ids',[]))
        for record in data:
            print(record)
        print("fi")
        
        """if self.product.id in (3365, 3364, 3247, 1276, 1277, 3352, 3379):
            res.update({'reparation_test_basic': [(0, 0, {'tname': 'WIFI'}), (0, 0, {'tname': 'Teclado'}), (0, 0, {'tname': 'Touchpad'}), (0, 0, {'tname': 'Pantalla táctil (Si lo és)'}), (0, 0, {'tname': 'Prueba carga (cargador original)'}), (0, 0, {
                'tname': 'Prueba de carga (superior al 10%) 5% D 5% IZ'}), (0, 0, {'tname': 'Tornillos'}), (0, 0, {'tname': 'Embalaje'}), (0, 0, {'tname': 'Modo tablet (Táctil y que funcione KB y TP)'}), (0, 0, {'tname': 'Equipo de sustitución'})]})
        else:
            res.update({'reparation_test_basic': [(0, 0, {'tname': 'WIFI'}), (0, 0, {'tname': 'Teclado'}), (0, 0, {'tname': 'Touchpad'}), (0, 0, {'tname': 'Prueba carga (cargador original)'}), (0, 0, {
                'tname': 'Prueba de carga (superior al 10%) 5% D 5% IZ'}), (0, 0, {'tname': 'Tornillos'}), (0, 0, {'tname': 'Embalaje'}), (0, 0, {'tname': 'Equipo de sustitución'})]})

        res.update({'reparation_test_user': [(0, 0, {'tname': 'Battery Test'}), (0, 0, {'tname': 'Cámara #1 (1ª opción web: probar cámara)'}), (0, 0, {
                   'tname': 'Cámara #2'}), (0, 0, {'tname': 'Micrófono (1ª opción web: probar micrófono)'}), (0, 0, {'tname': 'Audio (videos YouTube etc)'})]})"""

        return res

class getmrpdata(models.TransientModel):
    _name = 'getmrp.data.user'
    _description = "Get MRP Repair user Data"

    new_line_id_u = fields.Many2one('create.clreparation_mrp')
        
    ureparation = fields.One2many('cl.reparation','reparation_test_user', 'Reparacion') 
    tname = fields.Char("Test                       ", readonly="True")
    notes = fields.Char("Observaciones")
    yes = fields.Boolean("Si")
    no = fields.Boolean("No")

class getmrpdata(models.TransientModel):
    _name = 'getmrp.data.basic'
    _description = "Get MRP Repair basic Data"

    new_line_id_b = fields.Many2one('create.clreparation_mrp')
        
    ureparation = fields.One2many('cl.reparation','reparation_test_user', 'Reparacion') 
    tname = fields.Char("Test                       ", readonly="True")
    notes = fields.Char("Observaciones")
    yes = fields.Boolean("Si")
    no = fields.Boolean("No")