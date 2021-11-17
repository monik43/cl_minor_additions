# -*- coding: utf-8 -*-

import datetime, time
from dateutil import relativedelta
from odoo import api, fields, models, _
from odoo.exceptions import Warning


class helpdesk_stage(models.Model):
    _inherit = "helpdesk.stage"

    fold = fields.Boolean(
        "Folded", help="Folded in kanban view", compute="_compute_fold"
    )
    template_backup = fields.Many2one(
        "mail.template", compute="_compute_template_backup"
    )
    
    def _compute_template_backup(self):
        print(f'''
            /{str(self.template_id)}
        ''')
        if str(self.template_id) != "mail.template()":
            print("self.template_id != False, ", self.template_id)
            self.template_backup = self.template_id

    def _compute_fold(self):
        for rec in self:
            prev_fold = rec.fold
            if len(rec.env["helpdesk.ticket"].search([("stage_id", "=", rec.id)])) < 1:
                rec.fold = True
            elif (
                len(rec.env["helpdesk.ticket"].search([("stage_id", "=", rec.id)])) > 0
            ):
                rec.fold = False
    #@api.model
    @api.onchange('template_id')
    def onchange_template_id(self):
        print(f'''
            /{str(self.template_backup)}
        ''')
        if self.template_backup:
            self.template_id = self.template_backup

    @api.model
    def js_mail_template_disabler(self, rec_id):
        record = self.env["helpdesk.stage"].browse(rec_id)
        record.template_id = None
        print(f"""
            template_id ------> {record.template_id}
            template_backup --> {record.template_backup}
        """)
        return True

    @api.model
    def js_get_template_sequence(self, rec_id, target):
        return (
            self.env["helpdesk.stage"].browse(rec_id).sequence,
            self.env["helpdesk.stage"].browse(target).sequence,
        )

    @api.model
    def js_template_handler(self, id_stage):
        return (
            self.env["helpdesk.stage"].browse(id_stage).template_id.id,
            self.env["helpdesk.stage"].browse(id_stage).name,
        )


class helpdesk_ticket(models.Model):
    _inherit = "helpdesk.ticket"

    name_rma = fields.Char(compute="_get_name_rma")
    prod_id_context = fields.Many2one(
        "product.product", "Producto a reparar", compute="_get_prod_id_context"
    )
    lot_id_context = fields.Many2one("stock.production.lot", "Lote/Nº de serie	")
    self_cont = fields.Many2one("helpdesk.ticket", compute="_get_self_cont")

    # ordensat = fields.Many2one('mrp.repair', string='Orden SAT', compute="_get_orden_sat", ondelete='set null')
    sla_active = fields.Boolean(
        string="SLA active", compute="_compute_sla_fail", store=True, default=True
    )

    ordensat = fields.Many2many(
        "mrp.repair", string="Orden SAT", compute="_get_orden_sat", ondelete="set null"
    )

    @api.model
    def js_stage_handler(self, id):
        return self.env["helpdesk.ticket"].browse(id).x_lot_id.id

    @api.depends("deadline", "stage_id.sequence", "sla_id.stage_id.sequence")
    def _compute_sla_fail(self):
        if not self.user_has_groups("helpdesk.group_use_sla"):
            return
        for ticket in self:
            ticket.sla_active = True
            if not ticket.deadline:
                ticket.sla_active = False
                ticket.sla_fail = False
            elif ticket.sla_id.stage_id.sequence <= ticket.stage_id.sequence:
                if not ticket.sla_active:
                    ticket.sla_active = True
                prev_stage_ids = self.env["helpdesk.stage"].search(
                    [("sequence", "<", ticket.sla_id.stage_id.sequence)]
                )
                next_stage_ids = self.env["helpdesk.stage"].search(
                    [("sequence", ">=", ticket.sla_id.stage_id.sequence)]
                )
                stage_id_tracking_value = (
                    self.env["mail.tracking.value"]
                    .sudo()
                    .search(
                        [
                            ("field", "=", "stage_id"),
                            ("old_value_integer", "in", prev_stage_ids.ids),
                            ("new_value_integer", "in", next_stage_ids.ids),
                            ("mail_message_id.model", "=", "helpdesk.ticket"),
                            ("mail_message_id.res_id", "=", ticket.id),
                        ],
                        order="create_date ASC",
                        limit=1,
                    )
                )

                if ticket.sla_id.id == 3 and ticket.stage_id.sla_id:
                    ticket.sla_id = ticket.stage_id.sla_id
                    if not ticket.sla_active:
                        ticket.sla_active = True
                        ticket.sla_fail = False

                if stage_id_tracking_value:
                    if stage_id_tracking_value.create_date > ticket.deadline:
                        ticket.sla_fail = True
                # If there are no tracking messages, it means we *just* (now!) changed the state
                elif ticket.deadline and fields.Datetime.now() > ticket.deadline:
                    ticket.sla_fail = True

    def _get_orden_sat(self):
        for rec in self:
            if (
                rec.env["mrp.repair"].search([("x_ticket", "=", rec.id)])
                and len(rec.env["mrp.repair"].search([("x_ticket", "=", rec.id)])) == 1
            ):
                rec.update(
                    {
                        "ordensat": [
                            (
                                4,
                                rec.env["mrp.repair"]
                                .search([("x_ticket", "=", rec.id)])
                                .id,
                            )
                        ]
                    }
                )
            elif (
                rec.env["mrp.repair"].search([("x_ticket", "=", rec.id)])
                and len(rec.env["mrp.repair"].search([("x_ticket", "=", rec.id)])) > 1
            ):
                for rep in rec.env["mrp.repair"].search([("x_ticket", "=", rec.id)]):
                    rec.update({"ordensat": [(4, rep.id)]})
            elif rec.stage_id.name == "Diagnóstico":
                if rec.x_lot_id.id:
                    vals = {
                        "x_ticket": rec.id,
                        "product_id": rec.prod_id_context.id,
                        "lot_id": rec.x_lot_id.id,
                        "name": rec.name_rma,
                        "partner_id": rec.partner_id.id,
                        "product_qty": 1,
                        "product_uom": rec.prod_id_context.uom_id.id,
                        "company_id": 1,
                        "invoice_method": "none",
                        "pricelist_id": 1,
                        "internal_notes": 'Reparación creada cuando el estado del ticket relacionado se cambió a "Asignado".',
                    }
                    repar = rec.env["mrp.repair"].create(vals)
                    # rec.ordensat = repar
                    rec.update({"ordensat": [(4, repar.id)]})

    def _get_name_rma(self):
        for rec in self:
            if rec.RMA:
                rec.name_rma = str(rec.id) + " - " + str(rec.RMA)
            else:
                rec.name_rma = str(rec.id) + " - "

    def _get_prod_id_context(self):
        for rec in self:
            if rec.x_lot_id != False:
                rec.prod_id_context = rec.x_lot_id.product_id

    def _get_self_cont(self):
        for rec in self:
            rec.self_cont = self
