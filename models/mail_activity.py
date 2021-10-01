# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class mail_activity(models.Model):
    _inherit = 'mail.activity'

    filtro_check = fields.Boolean('Habilitar usuarios externos?')
    create_user_id = fields.Many2one('res.users', 'Creado por',default=lambda self: self.env.user,index=True, required=True)
    #activity_init_uid = fields.Many2one('res.users')
    #activity_init_date = fields.Datetime('Fecha creación', required=True, readonly=True)

    @api.onchange('filtro_check')
    def onchange_filtro_check(self):
        for record in self:
            if record.filtro_check:
                domain = [('firstname', '!=', False)]
            else:
                domain = [('share', '=', False)]
            return {'domain': {'user_id': domain}}
