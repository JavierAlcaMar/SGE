# -*- coding: utf-8 -*-
# from odoo import http


# class Guarderia(http.Controller):
#     @http.route('/guarderia/guarderia', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/guarderia/guarderia/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('guarderia.listing', {
#             'root': '/guarderia/guarderia',
#             'objects': http.request.env['guarderia.guarderia'].search([]),
#         })

#     @http.route('/guarderia/guarderia/objects/<model("guarderia.guarderia"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('guarderia.object', {
#             'object': obj
#         })

