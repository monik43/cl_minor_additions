# -*- coding: utf-8 -*-

import datetime
from dateutil import relativedelta
from odoo import api, fields, models, _


class helpdesk_stage(models.Model):
    _inherit = "helpdesk.stage"

    fold = fields.Boolean(
        'Folded', help='Folded in kanban view', compute="_compute_fold")

    def _compute_fold(self):
        for rec in self:
            prev_fold = rec.fold
            if len(rec.env['helpdesk.ticket'].search([('stage_id', '=', rec.id)])) < 1:
                rec.fold = True
            elif len(rec.env['helpdesk.ticket'].search([('stage_id', '=', rec.id)])) > 0:
                rec.fold = False

    @api.model
    def js_template_handler(self, id_stage):
        return self.env['helpdesk.stage'].browse(id_stage).template_id.id


class helpdesk_ticket(models.Model):
    _inherit = "helpdesk.ticket"

    name_rma = fields.Char(compute="_get_name_rma")
    prod_id_context = fields.Many2one(
        'product.product', "Producto a reparar", compute="_get_prod_id_context")
    lot_id_context = fields.Many2one(
        'stock.production.lot', "Lote/Nº de serie	", compute="_get_lot_id_context")
    self_cont = fields.Many2one('helpdesk.ticket', compute="_get_self_cont")
    
    #ordensat = fields.Many2one('mrp.repair', string='Orden SAT', compute="_get_orden_sat", ondelete='set null')

    ordensat = fields.Many2many(
        'mrp.repair', string='Orden SAT', compute="_get_orden_sat", ondelete='set null')

    def _get_orden_sat(self):
        for rec in self:
            if rec.env['mrp.repair'].search([('x_ticket', '=', rec.id)]):
                rec.ordensat = rec.env['mrp.repair'].search(
                    [('x_ticket', '=', rec.id)])
            """elif rec.stage_id.name == 'Asignado':
                vals = {
                    'x_ticket': rec.id,
                    'product_id': rec.prod_id_context.id,
                    'n_lot_id': rec.lot_id_context.id,
                    'name': rec.name_rma,
                    'partner_id': rec.partner_id.id,
                    'product_qty': 1,
                    'product_uom': rec.prod_id_context.uom_id.id,
                    'company_id':1,
                    'invoice_method':'none',
                    'pricelist_id': 1,
                    'internal_notes': "Reparación creada cuando el estado del ticket relacionado se cambió a \"Asignado\"."
                }
                repar = rec.env['mrp.repair'].create(vals)
                rec.ordensat = repar"""

    def _get_name_rma(self):
        for rec in self:
            if rec.RMA != False:
                rec.name_rma = str(rec.id) + " - " + str(rec.RMA)
            else:
                rec.name_rma = str(rec.id) + " - "

    def _get_prod_id_context(self):
        for rec in self:
            if rec.x_lot_id != False:
                rec.prod_id_context = rec.x_lot_id.product_id


    def _get_lot_id_context(self):
        for rec in self:
            if rec.x_lot_id != False:
                rec.lot_id_context = rec.env['stock.production.lot'].browse(
                    rec.x_lot_id.id)

    def _get_self_cont(self):
        for rec in self:
            rec.self_cont = self
