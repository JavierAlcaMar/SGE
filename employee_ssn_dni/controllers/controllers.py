# -*- coding: utf-8 -*-
# from odoo import http


# class EmployeeSsnDni(http.Controller):
#     @http.route('/employee_ssn_dni/employee_ssn_dni', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/employee_ssn_dni/employee_ssn_dni/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('employee_ssn_dni.listing', {
#             'root': '/employee_ssn_dni/employee_ssn_dni',
#             'objects': http.request.env['employee_ssn_dni.employee_ssn_dni'].search([]),
#         })

#     @http.route('/employee_ssn_dni/employee_ssn_dni/objects/<model("employee_ssn_dni.employee_ssn_dni"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('employee_ssn_dni.object', {
#             'object': obj
#         })

