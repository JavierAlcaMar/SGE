from odoo import models, fields

class Ejemplo(models.Model):
    _name = 'mi_modulo.ejemplo'
    _description = 'Modelo ejemplo para SGE'

    name = fields.Char(string="Nombre")
    edad = fields.Integer(string="Edad")
    activo = fields.Boolean(string="Activo", default=True)
