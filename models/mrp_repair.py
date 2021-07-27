# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.osv import orm
from lxml import etree


class repair_line(models.Model):
    _inherit = 'mrp.repair.line'

    pieza_añadida = fields.Boolean('Pieza añadida?')

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
            args = self.repair_id.company_id and [('company_id', '=', self.repair_id.company_id.id)] or []
            warehouse = self.env['stock.warehouse'].search(args, limit=1)
            self.location_id = self.repair_id.location_id
            self.location_dest_id = self.env['stock.location'].search([('usage', '=', 'production')], limit=1).id
        else:
            self.price_unit = 0.0
            self.tax_id = False
            self.location_id = self.env['stock.location'].search([('usage', '=', 'production')], limit=1).id
            self.location_dest_id = self.env['stock.location'].search([('scrap_location', '=', True)], limit=1).id

class mrp_repair(models.Model):
    _inherit = 'mrp.repair'

    n_lot_id = fields.Many2one(
        'stock.production.lot', 'Lote/Nº de serie',
        domain="[('product_id','=', product_id)]",
        help="Los productos reparados pertenecen todos a este lote")

    po_rel = fields.Many2one(
        'purchase.order', string='Purchase relacionada', compute="_compute_po_rel")

    def _compute_po_rel(self):
        for rec in self:
            if rec.env['purchase.order'].search([('partner_ref','like',rec.name)]) != "purchase.order()":
                rec.po_rel = rec.env['purchase.order'].search([('partner_ref','like',rec.name)])

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
                print("holi")
                node = doc.xpath("//button[@name='1122']")[0]
                for rec in self:
                    print("porel ",rec.po_rel)
                    if rec.po_rel != False:
                        node.set('class','')
                    else:
                        node.set('class','btn-primary')
        
        result['arch'] = etree.tostring(doc)
        return result

    