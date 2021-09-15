# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class user_credentials(models.Model):
    _name = 'cl.user.credentials'
    _description = 'Credenciales de usuario'

    name = fields.Char('Dominio Google Admin')
    mail = fields.Char('Correo electrónico', readonly=True)
    password = fields.Char('Contraseña', readonly=True)
