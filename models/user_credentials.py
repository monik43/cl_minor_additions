# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class user_credentials(models.Model):
    _name = 'cl.user.credentials'
    _description = 'Credenciales de usuario'

    name = fields.Char('Dominio Google Admin')
    mail = fields.Char('Correo electrónico')
    password = fields.Char('Contraseña')

    def _get_name(self):
        for rec in self:
            name_number = rec.desc, " ", 1
            if rec.name == False and rec.desc != False and not rec.env['cl.user.credentials'].search([('name', '=', rec.desc)]):
                print(rec.desc)#
                #rec.name = rec.desc
            elif rec.name == False and rec.desc != False and not rec.env['cl.user.credentials'].search([('name', '=', name_number)]):
                print(name_number)#
                #rec.name = name_number
            elif rec.name == False and rec.desc != False and rec.env['cl.user.credentials'].search([('name', '=', name_number)]):
                for x in range(10):
                    name_number = rec.desc+" "+ str(x+1)
                    if not rec.env['cl.user.credentials'].search([('name', '=', name_number)]):
                        print(name_number)#
                        #rec.name = name_number
                        break
