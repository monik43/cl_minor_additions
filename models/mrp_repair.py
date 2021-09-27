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

    lot_id = fields.Many2one('stock.production.lot', 'Lot/Serial', compute="_get_lot_id")
    po_rel = fields.Boolean(compute="_compute_po_rel")
    test_end = fields.Boolean(compute="_get_test_end")
    rep_conf = fields.Boolean(default=False, compute="_get_state")
    rec = fields.Many2one('mrp.repair', compute="_get_rec")
    rma = fields.Char(compute="_get_rma")
    reparation = fields.One2many('cl.reparation', 'origen_rep', "Reparaciones")
    purchase_orders = fields.Many2many('purchase.order', compute="_get_purchase_orders", ondelete='set null')

    def _get_purchase_orders(self):
        for rec in self:
            for line in rec.env['purchase.order'].search([('partner_ref', '=', rec.name)]):
                rec.update({'purchase_orders':[(4, line.id)]})
                
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

    @api.model
    def default_get(self,  fields):
        res = super(mrp_repair, self).default_get(fields)
        print(res)
        return res

    @api.multi
    def open_act(self):
        for rec in self:
            url = self.env['ir.config_parameter'].sudo().get_param(
                'web.base.url')
            rec_url = url + "/web#id=" + \
                str(self.id) + "&view_type=form&model=mrp.repair"
            client_action = {
                'type': 'ir.actions.act_url',
                'name': self.display_name,
                'target': 'new',
                'url': rec_url,
            }

            return client_action
