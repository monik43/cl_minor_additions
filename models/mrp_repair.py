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
                rec.po_rel = rec.env['purchase.order'].search([('origin', '=', rec.name)])
    
    @api.multi
    def test(self):
        result = super(mrp_repair, self).fields_view_get()
        doc = etree.XML(result['arch'])
        if self._module == 'cl_minor_additions':
            if doc.xpath("//button[@name='1122']"):
                node = doc.xpath("//button[@name='1122']")[0]
                if self.po_rel != False and node.get('class') == "btn-primary":
                    node.set('class','')

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False,
                        submenu=False):
        result = super(mrp_repair, self).fields_view_get(view_id,
                                                            view_type,
                                                            toolbar=toolbar,
                                                            submenu=submenu)

        doc = etree.XML(result['arch'])
        if view_type == 'form' and self._module == 'cl_minor_additions':
            if doc.xpath("//button[@name='1122']"):
                node = doc.xpath("//button[@name='1122']")[0]
                if self.po_rel != False and node.get('class') == "btn-primary":
                    node.set('class','')
                elif self.po_rel == False and node.get('class') != "btn-primary":
                    node.set('class','btn-primary')
        result['arch'] = etree.tostring(doc)
        return result