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

    ticket_x = fields.Many2one('helpdesk.ticket', compute="_get_ticket_x")
    lot_id = fields.Many2one('stock.production.lot', 'Lot/Serial', compute="_get_lot_id")
    po_rel = fields.Boolean(compute="_compute_po_rel")
    test_end = fields.Boolean(compute="_get_test_end")
    rep_conf = fields.Boolean(default=False, compute="_get_state")
    rec = fields.Many2one('mrp.repair', compute="_get_rec")
    rma = fields.Char(compute="_get_rma")
    reparation = fields.One2many('cl.reparation', 'origen_rep', "Reparaciones")
    purchase_orders = fields.Many2many('purchase.order', compute="_get_purchase_orders", ondelete='set null')
    sn_x = fields.Char(compute="_get_sn_x", store=True)

    def _get_sn_x(self):
        for rec in self:
            if rec.lot_id:
                rec.sn_x = rec.lot_id.name

    def _get_ticket_x(self):
        for rec in self:
            name = rec.name[:10].replace(" ","")
            s = 0
            chars = False
            nid = [c for c in rec.name if c.isdigit()][:4]
            test = [c for c in rec.name[:10] if c.isdigit()]
            sid = ''.join(str(c) for c in nid)
            """
            / or - in name :10 -> #2491-E
            / or - in name :10 -> 2382-ESB
            / or - in name :10 -> 2494-

            / or - in name :10 -> 10503/mal
            / or - in name :10 -> S134/mal
            / or - in name :10 -> 10523-ANUL
            / or - in name :10 -> 10559/2
            """
            if name.startswith("#"):
                name = name[1:]

            if name.find("/") > 0:
                i = name.find("/")
                name = name[:i]

            if name.find("-") > 0:
                i = name.find("-")
                name = name[:i]

            while s in range(len(name)):
                if not name[s].isdigit():
                    chars = True
                s=s+1

            if not chars:
                if not rec.x_ticket and self.env['helpdesk.ticket'].search([('id','=', name)]):
                    rec.ticket_x = self.env['helpdesk.ticket'].search([('id','=', name)])
            print(f"ticket_x . {rec.ticket_x.name}")

    @api.onchange('lot_id')
    def testuwu(self):
        for rec in self:
            print(rec.lot_id)

    def _get_lot_id(self):
        for rec in self:
            if not rec.lot_id and rec.x_ticket:
                if rec.x_ticket.x_lot_id:
                    rec.lot_id = rec.x_ticket.x_lot_id
                elif rec.x_ticket.x_sn and self.env['stock.production.lot'].search([('name','=',rec.x_ticket.x_sn.upper()),('product_id', '=', rec.product_id.id)]):
                    rec.lot_id = self.env['stock.production.lot'].search([('name','=',rec.x_ticket.x_sn.upper()),('product_id', '=', rec.product_id.id)])
            elif not rec.lot_id and rec.ticket_x:
                if rec.ticket_x.x_lot_id:
                    rec.lot_id = rec.ticket_x.x_lot_id
                elif not rec.ticket_x.x_lot_id and rec.ticket_x.x_sn and self.env['stock.production.lot'].search([('name','=',rec.ticket_x.x_sn.upper()),('product_id.id', '=', rec.product_id.id)]):
                    rec.lot_id = self.env['stock.production.lot'].search([('name','=',rec.ticket_x.x_sn.upper()),('product_id.id', '=', rec.product_id.id)])
            else:
                rec.lot_id = rec.lot_id

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
