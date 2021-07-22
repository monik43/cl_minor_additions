# -*- coding: utf-8 -*-

import datetime
from dateutil import relativedelta
from odoo import api, fields, models, _
from odoo.addons.helpdesk.models.helpdesk_ticket import TICKET_PRIORITY
from odoo.addons.http_routing.models.ir_http import slug
from odoo.exceptions import UserError, ValidationError


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
    lot_id_context = fields.Many2one('stock.production.lot', "Lote/Número de serie", compute="_get_lot_id_context")

    def _get_lot_id_context(self):
        for rec in self:
            rec.lot_id_context = rec.x_lot_id

    def _get_name_rma(self):
        for rec in self:
            if rec.RMA != False:
                rec.name_rma = str(rec.id) + " - " + str(rec.RMA)
            else:
                rec.name_rma = str(rec.id) + " - " + str(rec.name[:10])
