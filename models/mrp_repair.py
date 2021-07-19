# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.osv import orm
from lxml import etree


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

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False,
                        submenu=False):
        result = super(mrp_repair, self).fields_view_get(view_id,
                                                            view_type,
                                                            toolbar=toolbar,
                                                            submenu=submenu)

        doc = etree.XML(result['arch'])
        if view_type == 'form' and self._module == 'mrp.repair':
            if doc.xpath("//button[@name='1122']"):
                for placeholder in doc.xpath(
                        "//field[@name='amount_currency']"):
                    elem = etree.Element(
                        'field', {
                            'name': 'balance',
                            'readonly': 'True'
                        })
                    orm.setup_modifiers(elem)
                    placeholder.addprevious(elem)
            if not doc.xpath("//field[@name='amount_residual_currency']"):
                for placeholder in doc.xpath(
                        "//field[@name='amount_currency']"):
                    elem = etree.Element(
                        'field', {
                            'name': 'amount_residual_currency',
                            'readonly': 'True'
                        })
                    orm.setup_modifiers(elem)
                    placeholder.addnext(elem)
            if not doc.xpath("//field[@name='amount_residual']"):
                for placeholder in doc.xpath(
                        "//field[@name='amount_currency']"):
                    elem = etree.Element(
                        'field', {
                            'name': 'amount_residual',
                            'readonly': 'True'
                        })
                    orm.setup_modifiers(elem)
                    placeholder.addnext(elem)
            # Remove credit and debit data - which is irrelevant in this case
            for elem in doc.xpath("//field[@name='debit']"):
                doc.remove(elem)
            for elem in doc.xpath("//field[@name='credit']"):
                doc.remove(elem)
            result['arch'] = etree.tostring(doc)
        return result