# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class repair_line(models.Model):
    _inherit = 'mrp.repair.line'

    pieza_añadida = fields.Boolean('Pieza añadida?')

class mrp_repair(models.Model):
    _inherit = 'mrp.repair'
    po_rel = fields.Many2one(
        'purchase.order', string='Purchase relacionada', compute="_compute_po_rel")

    def _compute_po_rel(self):
        for rec in self:
            if rec.env['purchase.order'].search([('origin', '=', rec.name)]):
                rec.ticket_rel = rec.env['purchase.order'].search([('origin', '=', rec.name)])

    @api.multi
    def test(self):
        self.ensure_one()
        vres = super(mrp_repair, self).fields_view_get(view_id=3838)
        for field in vres:
            print("v ", field, " = ", vres[field])
        """if self.env['purchase.order'].search([('origin', '=', self.name)]) == 'selection1':
            action = {
                'name': _('Action 1'),
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'my.model',
                # 'view_id': # optional
                'type': 'ir.actions.act_window',
                # 'res_id': # optional
                'target': 'new'  # or 'current'
            }
        elif self.my_selection_field == 'selection2':
            action = {
                'name': _('Action 2'),
                'view_type': 'form',
                'view_mode': 'tree',
                'res_model': 'my.model',
                # 'view_id': # optional
                'type': 'ir.actions.act_window',
                # 'res_id': # optional
                'target': 'current'  # or 'new'
            }
        # and so on
        return action"""