# -*- coding: utf-8 -*-
# from odoo import http


# class Nominas(http.Controller):
#     @http.route('/nominas/nominas', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nominas/nominas/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('nominas.listing', {
#             'root': '/nominas/nominas',
#             'objects': http.request.env['nominas.nominas'].search([]),
#         })

#     @http.route('/nominas/nominas/objects/<model("nominas.nominas"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nominas.object', {
#             'object': obj
#         })

