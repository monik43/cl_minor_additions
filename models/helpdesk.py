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
            if rec.env['helpdesk.ticket'].search([('stage_id','=',rec.id)]) < 1:
                rec.fold = True
