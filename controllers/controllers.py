# -*- coding: utf-8 -*-
from odoo import http

# class ClMinorAdditions(http.Controller):
#     @http.route('/cl_minor_additions/cl_minor_additions/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cl_minor_additions/cl_minor_additions/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cl_minor_additions.listing', {
#             'root': '/cl_minor_additions/cl_minor_additions',
#             'objects': http.request.env['cl_minor_additions.cl_minor_additions'].search([]),
#         })

#     @http.route('/cl_minor_additions/cl_minor_additions/objects/<model("cl_minor_additions.cl_minor_additions"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cl_minor_additions.object', {
#             'object': obj
#         })