# -*- coding: utf-8 -*-
# from odoo import http


# class PcManagement(http.Controller):
#     @http.route('/pc_management/pc_management', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pc_management/pc_management/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('pc_management.listing', {
#             'root': '/pc_management/pc_management',
#             'objects': http.request.env['pc_management.pc_management'].search([]),
#         })

#     @http.route('/pc_management/pc_management/objects/<model("pc_management.pc_management"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pc_management.object', {
#             'object': obj
#         })

