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
        'cl.user.credentials', 'Credenciales test usuario', default=lambda self: self.env['cl.user.credentials'].search([('name', '=', 'Generico')]))
    reparation_test_basic = fields.One2many(
        'getmrp.data', 'breparation', 'Test')
    reparation_test_user = fields.One2many(
        'getmrp.data', 'ureparation', 'Test')
    product = fields.Many2one('product.product', 'Producto a reparar')
    test_complete = fields.Boolean(compute="_get_compute")

    @api.onchange('reparation_test_user','reparation_test_basic', 'usr_credentials')
    def _get_compute(self):
        for rec in self:
            passed = True
            for line in rec.reparation_test_basic:
                if not line.res:
                    passed = False
                    break
            
            if rec.usr_credentials:
                for line in rec.reparation_test_user:
                    if not line.res:
                        passed = False
                        break

            rec.test_complete = passed

                    
    @api.multi
    def action_create_cl_reparation(self):  # TODO
        self.ensure_one()
        res = self.env['cl.reparation'].browse(
            self._context.get('id', []))
        test = self.env['cl.reparation.newtest'].browse(
            self._context.get('id', []))
        datamrp = self.env['mrp.repair'].browse(
            self._context.get('active_ids', []))
        origin = str(self.origen_rep.id)

        if self.env['cl.reparation.newtest'].search([(
                'origin', '=', str(self.origen_rep.id))]) != False:
            for num in range(50):
                if not self.env['cl.reparation.newtest'].search([(
                    'origin', '=', str(self.origen_rep.id)+"_"+str(num)
                )]):
                    origin = str(self.origen_rep.id)+"_"+str(num)
                    break
        else:
            origin = str(self.origen_rep.id)

        value_basic = []
        value_user = []

        for data in self.reparation_test_user:
            test.create({
                'name': data.name,
                'notes': data.notes,
                'res': data.res,
                'type': data.type,
                'origin': origin,
            })

        for data in self.reparation_test_basic:
            print(data.name)
            print(data.res)
            test.create({
                'name': data.name,
                'notes': data.notes,
                'res': data.res,
                'type': data.type,
                'origin': origin,
            })

        for test in self.env['cl.reparation.newtest'].search(['&',('type', '=', 'basic'),('origin','=',origin)]):
            value_basic.append(test.id)

        for test in self.env['cl.reparation.newtest'].search(['&',('type', '=', 'usr'),('origin','=',origin)]):
            value_user.append(test.id)

        res.create({
            'usr_credentials': self.usr_credentials.id,
            'tecnico': self.tecnico_rep.id,
            'origen_rep': datamrp.id,
            'ticket': self.origen_hdt,
            'date': self.date,
            'RMA': self.RMA,
            'reparation_test_user': [(6, 0, value_user)],
            'reparation_test_basic': [(6, 0, value_basic)]
        })

        # self.env['mrp.repair'].action_repair_end()
        return res

    @api.model
    def default_get(self, fields):
        res = super(createclreparation_mrp, self).default_get(fields)
        data = self.env['mrp.repair'].browse(
            self._context.get('active_ids', []))
        res.update({'origen_rep': data.id})
        basic_test_names = []
        usr_test_names = []
        for line in self.env['cl.default.newtest'].search([]):
            if line.type == "usr":
                usr_test_names.append((0, 0, {'name': line.name, 'type': line.type}))
            else:
                basic_test_names.append((0, 0, {'name': line.name, 'type': line.type}))

        res.update({'reparation_test_basic': basic_test_names})
        res.update({'reparation_test_user': usr_test_names})

        return res


class getmrpdata(models.TransientModel):
    _name = 'getmrp.data'
    _description = "Get MRP Repair user Data"

    ureparation = fields.Many2one(
        'create.clreparation_mrp', 'reparation_test_user')
    breparation = fields.Many2one(
        'create.clreparation_mrp', 'reparation_test_basic')
    name = fields.Char("Test                       ")
    notes = fields.Char("Observaciones")
    type = fields.Selection([('basic','Básico'),('usr','Usuario'),],'Tipo')
    res = fields.Selection(
        [('y', 'Si'), ('n', 'No'), ('na', 'No aplica'), ], 'Resultado')
    #yes = fields.Boolean("Si")
    #no = fields.Boolean("No")
    #no_aplica = fields.Boolean("No aplica")
