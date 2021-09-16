# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.osv import orm
from lxml import etree
from odoo.exceptions import UserError


class repair_line(models.Model):
    _inherit = 'mrp.repair.line'

    pieza_anyadida = fields.Boolean('Pieza añadida?')

    @api.onchange('type', 'repair_id')
    def onchange_operation_type(self):
        """ On change of operation type it sets source location, destination location
        and to invoice field.
        @param product: Changed operation type.
        @param guarantee_limit: Guarantee limit of current record.
        @return: Dictionary of values.
        """
        if not self.type:
            self.location_id = False
            self.location_dest_id = False
        elif self.type == 'add':
            self.onchange_product_id()
            args = self.repair_id.company_id and [
                ('company_id', '=', self.repair_id.company_id.id)] or []
            warehouse = self.env['stock.warehouse'].search(args, limit=1)
            self.location_id = self.repair_id.location_id
            self.location_dest_id = self.env['stock.location'].search(
                [('usage', '=', 'production')], limit=1).id
        else:
            self.price_unit = 0.0
            self.tax_id = False
            self.location_id = self.env['stock.location'].search(
                [('usage', '=', 'production')], limit=1).id
            self.location_dest_id = self.env['stock.location'].search(
                [('scrap_location', '=', True)], limit=1).id


class mrp_repair(models.Model):
    _inherit = 'mrp.repair'

    n_lot_id = fields.Many2one(
        'stock.production.lot', 'Lote/Nº de serie',
        domain="[('product_id','=', product_id)]",
        help="Los productos reparados pertenecen todos a este lote")
    po_rel = fields.Boolean(compute="_compute_po_rel")
    test_end = fields.Boolean(compute="_get_test_end")
    rep_conf = fields.Boolean(default=False, compute="_get_state")
    rec = fields.Many2one('mrp.repair', compute="_get_rec")
    rma = fields.Char(compute="_get_rma")
    reparation = fields.One2many('cl.reparation', 'origen_rep', "Reparaciones")

    def _get_test_end(self):
        for rec in self:
            for line in rec.reparation:
                if line.test_pasado == True:
                    rec.test_end = True
                    break

    def _get_rec(self):
        for rec in self:
            rec.rec = rec

    def _get_rma(self):
        for rec in self:
            if rec.x_ticket.RMA != False:
                rec.rma = rec.x_ticket.RMA

    def _compute_po_rel(self):
        for rec in self:
            if rec.env['purchase.order'].search([('partner_ref', 'like', rec.name)]) != False:
                rec.po_rel = True
    def _get_state(self):
        for rec in self:
            if rec.state == 'confirmed' and rec.rep_conf != True:
                rec.rep_conf = True

    @api.multi
    def open_act(self):
        return {
            'name': self.display_name,
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': self._name,
            'res_id': self.id,
            'target': 'current'
        }
