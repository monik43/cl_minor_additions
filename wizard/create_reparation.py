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
        'cl.reparation.test.basic', 'breparation', 'Test')
    reparation_test_user = fields.One2many(
        'cl.reparation.test.user', 'ureparation', 'Test')
    product = fields.Many2one('product.product', 'Producto a reparar')


    @api.multi
    def action_create_cl_reparation(self):
        self.ensure_one()
        res = self.env['cl.reparation'].browse(self._context.get('id', []))
        basic_data = []
        user_data = []

        for data in self.reparation_test_basic:
            basic_data.append([0, 0, {'breparation': data.breparation, 'tname': data.tname,
                              'notes': data.notes, 'yes': data.yes, 'no': data.no}])

        for data in self.reparation_test_user:
            user_data.append([0, 0, {'breparation': data.ureparation, 'tname': data.tname,
                             'notes': data.notes, 'yes': data.yes, 'no': data.no}])

        res.create({'usr_credentials': self.usr_credentials, 'tecnico': self.tecnico_reps, 'origen_rep': self.origen_rep,
                   'ticket': self.origen_hdt, 'date': self.date, 'RMA': self.RMA, 'reparation_test_basic': basic_data, 'reparation_test_user': user_data})
        return res

    @api.multi
    def action_create_reparation_test(self):
        print("test"*10)
        self.ensure_one()
        """print("a"*25)
        res = self.env['cl.reparation']
        test_basic, test_user = []
        print("b"*25)
        for line in self.reparation_test_basic:
            test_basic.append(
                [0, 0, {'tname': line.tname, 'yes': line.yes, 'no': line.no, 'notes': line.notes}])
        print("c"*25)
        for line in self.reparation_test_user:
            test_user.append(
                [0, 0, {'tname': line.tname, 'yes': line.yes, 'no': line.no, 'notes': line.notes}])
        print("d"*25)
        res.create({
            'tecnico': self.tecnico_rep,
            'origen_rep': self.origen_rep,
            'usr_credentials': self.usr_credentials,
            'ticket': self.origen_hdt,
            'date': self.date,
            'RMA': self.RMA,
            'reparation_test_basic': test_basic,
            'reparation_test_user': test_user})"""
        print("e"*25)
        #return res

    @api.model
    def default_get(self, fields):
        res = super(createclreparation_mrp, self).default_get(fields)
        if self.product.id in (3365, 3364, 3247, 1276, 1277, 3352, 3379):
            res.update({'reparation_test_basic': [(0, 0, {'tname': 'WIFI'}), (0, 0, {'tname': 'Teclado'}), (0, 0, {'tname': 'Touchpad'}), (0, 0, {'tname': 'Pantalla táctil (Si lo és)'}), (0, 0, {'tname': 'Prueba carga (cargador original)'}), (0, 0, {
                'tname': 'Prueba de carga (superior al 10%) 5% D 5% IZ'}), (0, 0, {'tname': 'Tornillos'}), (0, 0, {'tname': 'Embalaje'}), (0, 0, {'tname': 'Modo tablet (Táctil y que funcione KB y TP)'}), (0, 0, {'tname': 'Equipo de sustitución'})]})
        else:
            res.update({'reparation_test_basic': [(0, 0, {'tname': 'WIFI'}), (0, 0, {'tname': 'Teclado'}), (0, 0, {'tname': 'Touchpad'}), (0, 0, {'tname': 'Prueba carga (cargador original)'}), (0, 0, {
                'tname': 'Prueba de carga (superior al 10%) 5% D 5% IZ'}), (0, 0, {'tname': 'Tornillos'}), (0, 0, {'tname': 'Embalaje'}), (0, 0, {'tname': 'Equipo de sustitución'})]})
        res.update({'reparation_test_user': [(0, 0, {'tname': 'Battery Test'}), (0, 0, {'tname': 'Cámara #1 (1ª opción web: probar cámara)'}), (0, 0, {
                   'tname': 'Cámara #2'}), (0, 0, {'tname': 'Micrófono (1ª opción web: probar micrófono)'}), (0, 0, {'tname': 'Audio (videos YouTube etc)'})]})
        return res
