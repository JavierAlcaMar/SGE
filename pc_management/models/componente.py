from odoo import models, fields

class PcComponente(models.Model):
    _name = 'pc.componente'
    _description = 'Componente de ordenador'

    nombre = fields.Char(string="Nombre técnico", required=True)
    especificaciones = fields.Text(string="Especificaciones")
    precio = fields.Monetary(string="Precio", currency_field="currency_id")
    currency_id = fields.Many2one('res.currency', string="Moneda", default=lambda self: self.env.company.currency_id)

