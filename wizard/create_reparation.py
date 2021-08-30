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
        'res.users', 'Técnico', domain="[('share','=',False)]",
         default=lambda self: self.env.user.id)
    origen_rep = fields.Many2one(
        'mrp.repair', 'Reparación')
    date = fields.Datetime(
        "Fecha", default=lambda self: fields.datetime.now())
    RMA = fields.Char('RMA')
    usr_credentials = fields.Many2one(
        'cl.user.credentials', 'Credenciales test usuario')
    reparation_test_basic = fields.One2many(
        'getmrp.data', 'breparation', 'Test')
    reparation_test_user = fields.One2many(
        'getmrp.data', 'ureparation', 'Test')
    product = fields.Many2one('product.product', 'Producto a reparar')

    def _test(self):
        print("test"*25)

    @api.multi
    def action_create_cl_reparation(self):
        self.ensure_one()
        res1 = self.env['cl.reparation'].browse(self._context.get('id', []))
        test = self.env['cl.reparation.test'].browse(self._context.get('id', []))
        datamrp = self.env['mrp.repair'].browse(self._context.get('active_ids', []))
        for data in self.reparation_test_user:
            test.create({
                'name': data.name,
                'notes': data.notes,
                'yes': data.yes,
                'no': data.no
            })
            test.create({
                'name': data.name,
                'notes': data.notes,
                'yes': data.yes,
                'no': data.no
            })

        res1.create({
            'usr_credentials': self.usr_credentials,
            'tecnico': self.tecnico_rep.id,
            'origen_rep': datamrp.id,
            'ticket': self.origen_hdt,
            'date': self.date,
            'RMA': self.RMA,
            #'reparation_test_user': test,
            #'reparation_test_basic': res3
        })
        return res1

    @api.multi
    def tprint(self):
        for line in self.reparation_test_basic:
            print(line.name)
            print(line.notes)

    @api.model
    def default_get(self, fields):
        res = super(createclreparation_mrp, self).default_get(fields)
        data = self.env['mrp.repair'].browse(self._context.get('active_ids', []))

        if data.product_id.id in (3412, 1279, 3405, 104, 1227, 242, 3379, 19, 400, 3165, 403, 3102, 3247, 1276, 3365, 3364, 3086, 297, 324, 330):
            print("/"*50)
            res.update({'reparation_test_basic': [(0, 0, {'name': 'WIFI'}), (0, 0, {'name': 'Teclado'}), (0, 0, {'name': 'Touchpad'}), (0, 0, {'name': 'Pantalla táctil (Si lo és)'}), (0, 0, {'name': 'Prueba carga (cargador original)'}), (0, 0, {
                'name': 'Prueba de carga (superior al 10%) 5% D 5% IZ'}), (0, 0, {'name': 'Tornillos'}), (0, 0, {'name': 'Embalaje'}), (0, 0, {'name': 'Modo tablet (Táctil y que funcione KB y TP)'}), (0, 0, {'name': 'Equipo de sustitución'})]})
        else:
            res.update({'reparation_test_basic': [(0, 0, {'name': 'WIFI'}), (0, 0, {'name': 'Teclado'}), (0, 0, {'name': 'Touchpad'}), (0, 0, {'name': 'Prueba carga (cargador original)'}), (0, 0, {
                'name': 'Prueba de carga (superior al 10%) 5% D 5% IZ'}), (0, 0, {'name': 'Tornillos'}), (0, 0, {'name': 'Embalaje'}), (0, 0, {'name': 'Equipo de sustitución'})]})

        res.update({'reparation_test_user': [(0, 0, {'name': 'Battery Test'}), (0, 0, {'name': 'Cámara #1 (1ª opción web: probar cámara)'}), (0, 0, {
                   'name': 'Cámara #2'}), (0, 0, {'name': 'Micrófono (1ª opción web: probar micrófono)'}), (0, 0, {'name': 'Audio (videos YouTube etc)'})]})

        return res


class getmrpdata(models.TransientModel):
    _name = 'getmrp.data'
    _description = "Get MRP Repair user Data"

    ureparation = fields.Many2one('create.clreparation_mrp', 'reparation_test_user', 'Reparacion')
    breparation = fields.Many2one('create.clreparation_mrp', 'reparation_test_basic', 'Reparacion')
    name = fields.Char("Test                       ")
    notes = fields.Char("Observaciones")
    yes = fields.Boolean("Si")
    no = fields.Boolean("No")